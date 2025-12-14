from django.contrib import admin
from .models import User, LoginHistory, Product, Order, OrderItem, Payment

# Register your models so they appear in Django admin
admin.site.register(User)
admin.site.register(LoginHistory)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
