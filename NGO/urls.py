from django.urls import path 
from . import views

urlpatterns = [
    path('register/', views.ngo_registration_form, name='ngo_registration'),
    path('login/', views.ngo_login, name='NGO_Login'),
    path('home/', views.home, name='ngo_home'),
    path('category/Clothes/', views.category_clothes, name='category_clothes'),
    path('category/Ration/', views.category_ration, name='category_clothes'),
    path('category/Medical_Supplies/', views.category_medical_supplies, name='category_clothes'),
    path('category/Toys/', views.category_toys, name='category_clothes'),
    path('category/Daily_Use/', views.category_daily_use, name='category_clothes'),
    path('category/Stationary/', views.category_stationary, name='category_clothes'),
    path('category/Utensils/', views.category_utensils, name='category_clothes'),
    path('ngo_cart/', views.ngo_cart, name='ngo_cart'),
    path('order/', views.ngo_order, name='ngo_order')
]