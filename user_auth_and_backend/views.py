from django.shortcuts import render, redirect, HttpResponse
from .forms import RegisterForm, LoginForm
from .models import User, Global_Categories
from django.contrib import messages
from . import forms
from . import models
import hashlib

from .functions import findCurrentUser
from bson import ObjectId

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

                        
            # creating a JWTCompatibleUser 
            class JWTCompatibleUser:
                def __init__(self, user):
                    self.id = str(user.id) 
                    self.user_email = str(user.user_email) 
                
                @property
                def is_authenticated(self):
                    return True     


            ## creating token
            jwt_user = JWTCompatibleUser(user)
            refresh = RefreshToken.for_user(user)


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
                    
                    # creating a JWTCompatibleUser 
                    class JWTCompatibleUser:
                        def __init__(self, user):
                            self.id = str(user.id) 
                            self.user_email = user.user_email 
                        
                        @property
                        def is_authenticated(self):
                            return True     

                    
                    
                    jwt_user = JWTCompatibleUser(user)
                    refresh = RefreshToken.for_user(user)
                    
                    # ✅ Redirect with JWT tokens as cookies
                    ## returning reponse is very very important step, there's a subtle difference between return response and return redirect('/user/home'), as it may seem the same, but in reality it isn't. reponse actually contains  the cookies which in turn contains JWT token. So when we say return redirect('/user/home') it actually doesn't contain any cookies and hence as you can see the logic in the decorator, it will be just re-directed to /user/login
                    response = redirect('/user/home/')  # your protected route
                    response.set_cookie('access_token', str(refresh.access_token), httponly=False)
                    response.set_cookie('refresh_token', str(refresh), httponly=False)


                    return response
                else:
                    return render(request, 'user_login.html', {'form' : form, 'error_message' : "Incorrect password"})
            except Exception as e: 
                return render(request, 'user_login.html', {'form' : form, 'error_message' : "User not found"})

    form = LoginForm()
    return render(request, 'user_login.html', {'form' : form})


@jwt_required
def user_home(request):
    user_id = request.jwt_payload.get('user_id')

    print(findCurrentUser(request))

    return render(request, 'user_home.html', {'user_id' : user_id})




@jwt_required
def category_test(request):

    if request.method == 'POST':
        category_test_form = forms.TestForm(request.POST, request.FILES)

        if category_test_form.is_valid():
            data = category_test_form.cleaned_data
            donation = models.User_Donation(
                quantity = data['quantity'],
                drop_off_location = data['drop_off_location'],
                date = data['date'],
                item = 'TestItem',
            )

            donation.photo.put(data['photo'], content_type=data['photo'].content_type)
            
            current_user_id = findCurrentUser(request)

            if current_user_id != None:
                print(current_user_id)
                user = User.objects.get(id=ObjectId(current_user_id))
                print(user)
                user.user_donations.append(donation)

                user.save()

                print("Submitting the form ")
                return HttpResponse("Requestion sent successfully")

            return redirect('/user/login')
    
    category_test_form = forms.TestForm()
    return render(request, 'category_test.html', {'form' : category_test_form})

@jwt_required
def user_pending_requests(request):
    id = findCurrentUser(request)
    user_donations = models.User.objects.get(id=ObjectId(id)).user_donations# this contains the entire collection 
    return render(request, 'user_pending_requests.html', {'user_donations' : user_donations})

@jwt_required
def category_clothes(request):

    if request.method == 'POST':
        category_test_form = forms.TestForm(request.POST, request.FILES)

        if category_test_form.is_valid():
            data = category_test_form.cleaned_data
            donation = models.User_Donation(
                quantity = data['quantity'],
                drop_off_location = data['drop_off_location'],
                date = data['date'],
                item = 'Clothes',
            )


            donation.photo.put(data['photo'], content_type=data['photo'].content_type)

            current_user_id = findCurrentUser(request)
            print("Hello mi ithe ahe")
            if current_user_id != None:
                print(current_user_id)
                user = User.objects.get(id=ObjectId(current_user_id))
                print(user)
                user.user_donations.append(donation)

                user.save()

                category = Global_Categories.objects(id=ObjectId('6893495615af1913e64d9644'))
                print(category.quantity)

                print("Submitting the form ")
                return HttpResponse("Requestion sent successfully")

            return redirect('/user/login')
    
    category_test_form = forms.TestForm()
    return render(request, 'category_test.html', {'form' : category_test_form})

@jwt_required
def category_ration(request):

    if request.method == 'POST':
        category_test_form = forms.TestForm(request.POST, request.FILES)

        if category_test_form.is_valid():
            data = category_test_form.cleaned_data
            donation = models.User_Donation(
                quantity = data['quantity'],
                drop_off_location = data['drop_off_location'],
                date = data['date'],
                item = 'Ration',
            )

            donation.photo.put(data['photo'], content_type=data['photo'].content_type)

            current_user_id = findCurrentUser(request)

            if current_user_id != None:
                print(current_user_id)
                user = User.objects.get(id=ObjectId(current_user_id))
                print(user)
                user.user_donations.append(donation)

                user.save()

                print("Submitting the form ")
                return HttpResponse("Requestion sent successfully")

            return redirect('/user/login')

    
    category_test_form = forms.TestForm()
    return render(request, 'category_test.html', {'form' : category_test_form})

@jwt_required
def category_medical_supplies(request):

    if request.method == 'POST':
        category_test_form = forms.TestForm(request.POST, request.FILES)

        if category_test_form.is_valid():
            data = category_test_form.cleaned_data
            donation = models.User_Donation(
                quantity = data['quantity'],
                drop_off_location = data['drop_off_location'],
                date = data['date'],
                item = 'Medical Supplies',
            )

            donation.photo.put(data['photo'], content_type=data['photo'].content_type)

            current_user_id = findCurrentUser(request)

            if current_user_id != None:
                print(current_user_id)
                user = User.objects.get(id=ObjectId(current_user_id))
                print(user)
                user.user_donations.append(donation)

                user.save()

                print("Submitting the form ")
                return HttpResponse("Requestion sent successfully")

            return redirect('/user/login')

    
    category_test_form = forms.TestForm()
    return render(request, 'category_test.html', {'form' : category_test_form})

@jwt_required
def category_toys(request):

    if request.method == 'POST':
        category_test_form = forms.TestForm(request.POST, request.FILES)

        if category_test_form.is_valid():
            data = category_test_form.cleaned_data
            donation = models.User_Donation(
                quantity = data['quantity'],
                drop_off_location = data['drop_off_location'],
                date = data['date'],
                item = 'Toys',
            )

            donation.photo.put(data['photo'], content_type=data['photo'].content_type)

            current_user_id = findCurrentUser(request)

            if current_user_id != None:
                print(current_user_id)
                user = User.objects.get(id=ObjectId(current_user_id))
                print(user)
                user.user_donations.append(donation)

                user.save()

                print("Submitting the form ")
                return HttpResponse("Requestion sent successfully")

            return redirect('/user/login')

    
    category_test_form = forms.TestForm()
    return render(request, 'category_test.html', {'form' : category_test_form})

@jwt_required
def category_daily_use(request):

    if request.method == 'POST':
        category_test_form = forms.TestForm(request.POST, request.FILES)

        if category_test_form.is_valid():
            data = category_test_form.cleaned_data
            donation = models.User_Donation(
                quantity = data['quantity'],
                drop_off_location = data['drop_off_location'],
                date = data['date'],
                item = 'Daily Use',
            )

            donation.photo.put(data['photo'], content_type=data['photo'].content_type)

            current_user_id = findCurrentUser(request)

            if current_user_id != None:
                print(current_user_id)
                user = User.objects.get(id=ObjectId(current_user_id))
                print(user)
                user.user_donations.append(donation)

                user.save()

                print("Submitting the form ")
                return HttpResponse("Requestion sent successfully")

            return redirect('/user/login')

    
    category_test_form = forms.TestForm()
    return render(request, 'category_test.html', {'form' : category_test_form})

@jwt_required
def category_stationary(request):

    if request.method == 'POST':
        category_test_form = forms.TestForm(request.POST, request.FILES)

        if category_test_form.is_valid():
            data = category_test_form.cleaned_data
            donation = models.User_Donation(
                quantity = data['quantity'],
                drop_off_location = data['drop_off_location'],
                date = data['date'],
                item = 'Stationary',
            )

            donation.photo.put(data['photo'], content_type=data['photo'].content_type)

            current_user_id = findCurrentUser(request)

            if current_user_id != None:
                print(current_user_id)
                user = User.objects.get(id=ObjectId(current_user_id))
                print(user)
                user.user_donations.append(donation)

                user.save()

                print("Submitting the form ")
                return HttpResponse("Requestion sent successfully")

            return redirect('/user/login')

    
    category_test_form = forms.TestForm()
    return render(request, 'category_test.html', {'form' : category_test_form})

@jwt_required
def category_utensils(request):

    if request.method == 'POST':
        category_test_form = forms.TestForm(request.POST, request.FILES)

        if category_test_form.is_valid():
            data = category_test_form.cleaned_data
            donation = models.User_Donation(
                quantity = data['quantity'],
                drop_off_location = data['drop_off_location'],
                date = data['date'],
                item = 'Utensils',
            )

            donation.photo.put(data['photo'], content_type=data['photo'].content_type)

            current_user_id = findCurrentUser(request)

            if current_user_id != None:
                print(current_user_id)
                user = User.objects.get(id=ObjectId(current_user_id))
                print(user)
                user.user_donations.append(donation)

                user.save()

                print("Submitting the form ")
                return HttpResponse("Requestion sent successfully")

            return redirect('/user/login')

    
    category_test_form = forms.TestForm()
    return render(request, 'category_test.html', {'form' : category_test_form})


def temp_form(request):
    if request.method == 'POST':
        form = forms.Categories(request.POST)

        if form.is_valid():
            category = models.Global_Categories(
                category_name = form.cleaned_data['category_name'],
                category_quantity = form.cleaned_data['category_quantity']
            )
            category.save()

            return HttpResponse("happy")
    
    form = forms.RegisterForm()
    return render(request, 'temp_form.html', {'form' : form})