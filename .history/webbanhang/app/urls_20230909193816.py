from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('cart/', views.cart, name="cart"),
    path('/checkout', views.checkout, name="checkout"),
]
