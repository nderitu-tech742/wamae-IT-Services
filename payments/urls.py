from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_payment, name='add_payment'),
    path('list/', views.list_payments, name='list_payments'),
]
