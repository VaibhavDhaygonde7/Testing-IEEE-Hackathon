from django.urls import path
from . import views 

urlpatterns = [
    path('', views.admin_verification, name='admin-verfication'),
    path('home/', views.home, name='Admin_home'),
    path('photo/<str:photo_id>/', views.serve_photo, name='serve_photo'),
    path('approve/', views.admin_approve, name='admin_approve'),
]