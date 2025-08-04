from django.shortcuts import render, redirect, HttpResponse
from .forms import RegisterForm, LoginForm
from .models import User
from django.contrib import messages
import hashlib

from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .decorators import jwt_required
# Create your views here.

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def registration_form(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if User.objects(user_email=form.cleaned_data['user_email']):
                # messages.error(request, "Email Already exists")
                print("email already exist karto")
                return render(request, 'registration_form.html', {'form' : form, 'error_message' : "Email already exists" })
            
            user = User(
                user_name = form.cleaned_data['user_name'],
                user_email = form.cleaned_data['user_email'],
                user_password = hash_password(form.cleaned_data['user_password']),
                user_phone_number = form.cleaned_data['user_phone_number'],
            )

            user.save()

                        
            ## creating a JWTCompatibleUser 
            class JWTCompatibleUser:
                def __init__(self, user):
                    self.id = str(user.id) 
                    self.user_email = str(user.user_email) 
                
                @property
                def is_authenticated(self):
                    return True     


            ## creating token
            jwt_user = JWTCompatibleUser(user)
            refresh = RefreshToken.for_user(jwt_user)

            response = redirect('/user/login/')
            response.set_cookie('access_token', str(refresh.access_token), httponly=False)
            response.set_cookie('refrest_token', str(refresh), httponly=False)


            print("Redirecting...")
            return response


    form = RegisterForm()
    return render(request, 'registration_form.html', {'form' : form})

def login_view(request):
    if request.method == 'POST': 
        form = LoginForm(request.POST)

        if form.is_valid(): 
            instantaneous_user_email = form.cleaned_data['user_email']
            instantaneous_user_password = hash_password(form.cleaned_data['user_password'])

            try: 
                user = User.objects.get(user_email=instantaneous_user_email)
                if user.user_password == instantaneous_user_password:
                    
                    ## creating a JWTCompatibleUser 
                    class JWTCompatibleUser:
                        def __init__(self, user):
                            self.id = str(user.id) 
                            self.user_email = user.user_email 
                        
                        @property
                        def is_authenticated(self):
                            return True     

                    
                    jwt_user = JWTCompatibleUser(user)
                    refresh = RefreshToken.for_user(jwt_user)

                    # ✅ Redirect with JWT tokens as cookies
                    response = redirect('/home/')  # your protected route
                    response.set_cookie('access_token', str(refresh.access_token), httponly=False)
                    response.set_cookie('refresh_token', str(refresh), httponly=False)


                    return redirect('/user/home/')
                else:
                    return render(request, 'user_login.html', {'form' : form, 'error_message' : "Incorrect password"})
            except Exception as e: 
                return render(request, 'user_login.html', {'form' : form, 'error_message' : "User not found"})

    form = LoginForm()
    return render(request, 'user_login.html', {'form' : form})


@jwt_required
def user_home(request):
    user_id = request.jwt_payload.get('user_id')

    return render(request, 'user_home.html', {'user_id' : user_id})






# ithun mi gaand masti karat ahe
