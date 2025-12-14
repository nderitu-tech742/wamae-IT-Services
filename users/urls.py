from django.urls import path
from . import views

urlpatterns = [
    # -------------------- PUBLIC --------------------
    path('', views.home, name='home'),  # Public homepage

    # -------------------- AUTHENTICATION --------------------
    path('login/', views.custom_login, name='login'),        # Login page
    path('logout/', views.custom_logout, name='logout'),     # Logout
    path('register/', views.register_view, name='register'), # Register page

    # -------------------- DASHBOARDS --------------------
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard
    path('dashboard/', views.user_dashboard, name='user_dashboard'),          # User dashboard

    # -------------------- ADMIN ACTIONS --------------------
    path('add-product/', views.add_product, name='add_product'),  # Admin adds new product/service

    # -------------------- USER ACTIONS --------------------
    path('place-order/<int:product_id>/', views.place_order, name='place_order'),  # User places an order

    # -------------------- PAYMENT SYSTEM --------------------
    path('pay/<int:order_id>/', views.payment_page, name='payment_page'),                  # Shows payment page
    path('process-payment/<int:order_id>/', views.process_payment, name='process_payment'), # Handles payment processing
    path('payment-success/', views.payment_success, name='payment_success'),               # Final payment success page
]
