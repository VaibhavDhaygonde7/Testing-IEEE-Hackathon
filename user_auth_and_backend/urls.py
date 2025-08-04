from django.urls import path 
from . import views

urlpatterns = [
    path('register/', views.registration_form, name='registration'),
    path('login/', views.login_view, name='login'),
    path('home/', views.user_home, name='home')
]