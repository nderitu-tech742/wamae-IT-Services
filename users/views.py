import uuid
import urllib.parse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from functools import wraps
from .models import Product, Order, OrderItem, Payment
from django.contrib.auth import get_user_model

User = get_user_model()

# -------------------- HELPER FUNCTIONS --------------------
def redirect_dashboard(user):
    """Redirect users based on their role."""
    return redirect('admin_dashboard' if user.role == 'admin' else 'user_dashboard')

def role_required(role):
    """Decorator to restrict access to users with a specific role."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Please log in first.")
                return redirect('login')
            if request.user.role != role:
                messages.error(request, f"Access denied: {role.capitalize()}s only.")
                return redirect_dashboard(request.user)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# -------------------- HOME PAGE --------------------
def home(request):
    return render(request, 'users/home.html')

# -------------------- LOGIN --------------------
def custom_login(request):
    if request.user.is_authenticated:
        return redirect_dashboard(request.user)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect_dashboard(user)
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'users/login.html')

# -------------------- REGISTER --------------------
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please log in.")
            return redirect('login')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please log in.")
            return redirect('login')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.role = 'user'
        user.save()

        login(request, user)
        messages.success(request, f"Welcome, {user.username}! Your account was created successfully.")
        return redirect_dashboard(user)

    return render(request, 'users/register.html')

# -------------------- LOGOUT --------------------
@login_required(login_url='login')
def custom_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')

# -------------------- ADMIN DASHBOARD --------------------
@role_required('admin')
def admin_dashboard(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        new_payment_status = request.POST.get('payment_status')

        order = get_object_or_404(Order, id=order_id)

        if new_status:
            order.status = new_status
            order.save()
            messages.success(request, f"Order #{order.id} status updated to {new_status.capitalize()}.")

        if new_payment_status:
            if hasattr(order, 'payment'):
                order.payment.status = new_payment_status
                order.payment.save()
            else:
                Payment.objects.create(
                    order=order,
                    amount=order.total_amount,
                    method='cash',
                    status=new_payment_status
                )
            messages.success(request, f"Payment status for Order #{order.id} updated to {new_payment_status.capitalize()}.")

        return redirect('admin_dashboard')

    context = {
        'total_products': Product.objects.count(),
        'total_orders': Order.objects.count(),
        'total_payments': Payment.objects.count(),
        'pending_orders': Order.objects.filter(status='pending').count(),
        'orders': Order.objects.all().order_by('-created_at')
    }
    return render(request, 'users/admin_dashboard.html', context)

# -------------------- ADD PRODUCT --------------------
@role_required('admin')
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        image = request.FILES.get('image')

        if not name or not price or not quantity:
            messages.error(request, "Please fill in all required fields.")
            return redirect('add_product')

        product = Product.objects.create(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            image=image
        )
        messages.success(request, f"Product '{product.name}' added successfully!")
        return redirect('admin_dashboard')

    return render(request, 'users/add_product.html')

# -------------------- USER DASHBOARD --------------------
@role_required('user')
def user_dashboard(request):
    products = Product.objects.all()
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'users/user_dashboard.html', {'products': products, 'orders': orders})

# -------------------- PLACE ORDER --------------------
@role_required('user')
def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order = Order.objects.create(user=request.user, status='pending')
    OrderItem.objects.create(order=order, product=product, quantity=1)

    messages.success(request, f"Your order for {product.name} has been submitted! Proceed to payment.")
    return redirect('payment_page', order_id=order.id)

# -------------------- PAYMENT PAGE --------------------
@role_required('user')
def payment_page(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if hasattr(order, 'payment'):
        messages.info(request, "Payment already exists for this order.")
        return redirect('user_dashboard')

    return render(request, 'users/payment_page.html', {'order': order})

# -------------------- PROCESS PAYMENT (WITH PESA-PAL) --------------------
@role_required('user')
def process_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if hasattr(order, 'payment'):
        messages.info(request, "Payment already processed.")
        return redirect('user_dashboard')

    if request.method == 'POST':
        method = request.POST.get('method')
        if not method:
            messages.error(request, "Please select a payment method.")
            return redirect('payment_page', order_id=order.id)

        # Offline payments
        if method in ['cash', 'card']:
            Payment.objects.create(
                order=order,
                amount=order.total_amount,
                method=method,
                status='approved'
            )
            order.status = 'shipped'
            order.save()
            messages.success(request, "Payment successful! Your order will be processed shortly.")
            return redirect('payment_success')

        # PesaPal (Mpesa)
        if method == 'mpesa':
            tracking_id = str(uuid.uuid4())
            params = {
                'amount': order.total_amount,
                'description': f'Order #{order.id} payment',
                'type': 'MERCHANT',
                'reference': tracking_id,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'currency': settings.PESAPAL_CURRENCY,
                'callback_url': request.build_absolute_uri('/payment-success/')
            }

            query_string = urllib.parse.urlencode(params)
            payment_url = f"{settings.PESAPAL_POST_URL}?{query_string}"

            Payment.objects.create(
                order=order,
                amount=order.total_amount,
                method='mpesa',
                status='pending'
            )

            return redirect(payment_url)

    return redirect('payment_page', order_id=order.id)

# -------------------- PAYMENT SUCCESS --------------------
@login_required(login_url='login')
def payment_success(request):
    return render(request, 'users/payment_success.html')
