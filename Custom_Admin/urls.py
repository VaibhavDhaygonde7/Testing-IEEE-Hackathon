from django.urls import path
from . import views 

urlpatterns = [
    path('', views.admin_verification, name='admin-verfication'),
    path('home/', views.home, name='Admin_home'),
]