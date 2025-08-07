from django.urls import path 
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.registration_form, name='registration'),
    path('login/', views.login_view, name='login'),
    path('home/', views.user_home, name='home'),
    path('category/test/', views.category_test, name='category_test'),
    path('category/clothes/', views.category_clothes, name='category_test'),
    path('category/ration/', views.category_ration, name='category_test'),
    path('category/medical-supplies/', views.category_medical_supplies, name='category_test'),
    path('category/toys/', views.category_toys, name='category_test'),
    path('category/daily-use/', views.category_daily_use, name='category_test'),
    path('category/stationary/', views.category_stationary, name='category_test'),
    path('category/utensils/', views.category_utensils, name='category_test'),
    path('pending_requests/', views.user_pending_requests, name='pending_requests'),
    path('form/', views.temp_form, name='temp_form')
]