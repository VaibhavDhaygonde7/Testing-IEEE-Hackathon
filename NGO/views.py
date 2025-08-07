from django.shortcuts import render, HttpResponse, redirect
from . import forms 
from . import models
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .decorators import jwt_required
from .functions import findCurrentUser
import hashlib
from bson import ObjectId


# Create your views here.


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def ngo_registration_form(request):
    if request.method == 'POST':
        form = forms.NGORegistrationForm(request.POST)

        if form.is_valid():

            if models.NGO.objects(ngo_email = form.cleaned_data['ngo_email']):
                print("Email already exists")
                return render(request, 'ngo_registration_form.html', {'form' : form, 'error_message' : 'User already exists'})

            ngo = models.NGO(
                ngo_name = form.cleaned_data['ngo_name'],
                ngo_email = form.cleaned_data['ngo_email'],
                ngo_password = hash_password(form.cleaned_data['ngo_password']),
                ngo_phone_number = form.cleaned_data['ngo_phone_number'],
                ngo_address = form.cleaned_data['ngo_address'],
            )

            ngo.save()

            # creating a JWTCompatibleUser 
            class JWTCompatibleUser:
                def __init__(self, ngo):
                    self.id = str(ngo.id) 
                    self.ngo_email = str(ngo.ngo_email) 
                
                @property
                def is_authenticated(self):
                    return True     


            ## creating token
            jwt_user = JWTCompatibleUser(ngo)
            refresh = RefreshToken.for_user(ngo)


            response = redirect('/ngo/login/')
            response.set_cookie('access_token', str(refresh.access_token), httponly=False)
            response.set_cookie('refrest_token', str(refresh), httponly=False)


            print("Redirecting...")
            return response

    form = forms.NGORegistrationForm()
    return render(request, 'ngo_registration_form.html', {'form' : form})

def ngo_login(request):
    if request.method == 'POST':
        form = forms.NGOLogin(request.POST)

        if form.is_valid():
            instantaneous_ngo_email = form.cleaned_data['ngo_email']
            instantaneous_ngo_password = hash_password(form.cleaned_data['ngo_password'])

            ngo = models.NGO.objects(ngo_email = instantaneous_ngo_email)

            if ngo:
                ngo = ngo.first()
                if ngo.ngo_password == instantaneous_ngo_password:
                    # creating a JWTCompatibleUser 
                    class JWTCompatibleUser:
                        def __init__(self, ngo):
                            self.id = str(ngo.id) 
                            self.ngo_email = str(ngo.ngo_email) 
                        
                        @property
                        def is_authenticated(self):
                            return True     
                    
                    
                    jwt_user = JWTCompatibleUser(ngo)
                    refresh = RefreshToken.for_user(ngo)
                    
                    # ✅ Redirect with JWT tokens as cookies
                    ## returning reponse is very very important step, there's a subtle difference between return response and return redirect('/user/home'), as it may seem the same, but in reality it isn't. reponse actually contains  the cookies which in turn contains JWT token. So when we say return redirect('/user/home') it actually doesn't contain any cookies and hence as you can see the logic in the decorator, it will be just re-directed to /user/login
                    response = redirect('/ngo/home/')  # your protected route
                    response.set_cookie('access_token', str(refresh.access_token), httponly=False)
                    response.set_cookie('refresh_token', str(refresh), httponly=False)


                    return response
                
                else: 
                    print("NGO password incorrect")
                    return render(request, 'ngo_login.html', {'form' : form, 'error_message':'Password Incorrect'})
                    
            print("NGO not found")
            return render(request, 'ngo_login.html', {'form': form,'error_message':"NGO not found"})

        
    form = forms.NGOLogin()
    return render(request, 'ngo_login.html', {'form' : form})

@jwt_required
def home(request):
    ngo_id = findCurrentUser(request)

    categories = models.Global_Categories.objects()

    return render(request, 'ngo_home.html', {'ngo_id' : ngo_id, 'categories' : categories})

@jwt_required
def category_clothes(request):
    
    if request.method == 'POST':
        category_test_form = forms.TestForm(request.POST, request.FILES)

        if category_test_form.is_valid():
            data = category_test_form.cleaned_data
            current_user_id = findCurrentUser(request)

            if current_user_id != None:
                print(current_user_id)
                ngo = models.NGO.objects.get(id=ObjectId(current_user_id))
                print(ngo.ngo_name)

                category = models.Global_Categories.objects(id=ObjectId('6893495615af1913e64d9644')).first()
                print(category.category_quantity)
                print(data['category_quantity'])
                if category.category_quantity < data['category_quantity']:
                    print("select a lower quantity")
                    return render(request, 'ngo_category_test.html', {'form' : category_test_form, 'error_message' : f"Please select a quantity less than {category.category_quantity + 1}"})

                ngo_cart = models.NGO_Cart(
                    category_name = "Clothes",
                    category_quantity = data['category_quantity']
                )

                ngo.ngo_cart.append(ngo_cart)

                ngo.save()

                print("Submitting the form ")
                return render(request, 'ngo_category_test.html', {'success_message' : "Request sent successfully, check your cart🛒"})

            return redirect('/ngo/login')
    
    category_test_form = forms.TestForm()
    return render(request, 'ngo_category_test.html', {'form' : category_test_form, 'category' : "Clothes"})

@jwt_required
def category_ration(request):
    
    if request.method == 'POST':
        category_test_form = forms.TestForm(request.POST, request.FILES)

        if category_test_form.is_valid():
            data = category_test_form.cleaned_data
            current_user_id = findCurrentUser(request)

            if current_user_id != None:
                print(current_user_id)
                ngo = models.NGO.objects.get(id=ObjectId(current_user_id))
                print(ngo.ngo_name)

                category = models.Global_Categories.objects(id=ObjectId('6893497a15af1913e64d9645')).first()
                print(category.category_quantity)
                print(data['category_quantity'])
                if category.category_quantity < data['category_quantity']:
                    print("select a lower quantity")
                    return render(request, 'ngo_category_test.html', {'form' : category_test_form, 'error_message' : f"Please select a quantity less than {category.category_quantity + 1}"})

                ngo_cart = models.NGO_Cart(
                    category_name = "Ration",
                    category_quantity = data['category_quantity']
                )

                ngo.ngo_cart.append(ngo_cart)

                ngo.save()

                print("Submitting the form ")
                return render(request, 'ngo_category_test.html', {'success_message' : "Request sent successfully, check your cart🛒"})

            return redirect('/ngo/login')
    
    category_test_form = forms.TestForm()
    return render(request, 'ngo_category_test.html', {'form' : category_test_form, 'category' : "Ration"})

@jwt_required
def category_medical_supplies(request):
    
    if request.method == 'POST':
        category_test_form = forms.TestForm(request.POST, request.FILES)

        if category_test_form.is_valid():
            data = category_test_form.cleaned_data
            current_user_id = findCurrentUser(request)

            if current_user_id != None:
                print(current_user_id)
                ngo = models.NGO.objects.get(id=ObjectId(current_user_id))
                print(ngo.ngo_name)

                category = models.Global_Categories.objects(id=ObjectId('6893498515af1913e64d9646')).first()
                print(category.category_quantity)
                print(data['category_quantity'])
                if category.category_quantity < data['category_quantity']:
                    print("select a lower quantity")
                    return render(request, 'ngo_category_test.html', {'form' : category_test_form, 'error_message' : f"Please select a quantity less than {category.category_quantity + 1}"})

                ngo_cart = models.NGO_Cart(
                    category_name = "Medical_Supplies",
                    category_quantity = data['category_quantity']
                )

                ngo.ngo_cart.append(ngo_cart)

                ngo.save()

                print("Submitting the form ")
                return render(request, 'ngo_category_test.html', {'success_message' : "Request sent successfully, check your cart🛒"})

            return redirect('/ngo/login')
    
    category_test_form = forms.TestForm()
    return render(request, 'ngo_category_test.html', {'form' : category_test_form, 'category' : "Medical Supplies"})

@jwt_required
def category_toys(request):
    
    if request.method == 'POST':
        category_test_form = forms.TestForm(request.POST, request.FILES)

        if category_test_form.is_valid():
            data = category_test_form.cleaned_data
            current_user_id = findCurrentUser(request)

            if current_user_id != None:
                print(current_user_id)
                ngo = models.NGO.objects.get(id=ObjectId(current_user_id))
                print(ngo.ngo_name)

                category = models.Global_Categories.objects(id=ObjectId('6893498b15af1913e64d9647')).first()
                print(category.category_quantity)
                print(data['category_quantity'])
                if category.category_quantity < data['category_quantity']:
                    print("select a lower quantity")
                    return render(request, 'ngo_category_test.html', {'form' : category_test_form, 'error_message' : f"Please select a quantity less than {category.category_quantity + 1}"})

                ngo_cart = models.NGO_Cart(
                    category_name = "Toys",
                    category_quantity = data['category_quantity']
                )

                ngo.ngo_cart.append(ngo_cart)

                ngo.save()

                print("Submitting the form ")
                return render(request, 'ngo_category_test.html', {'success_message' : "Request sent successfully, check your cart🛒"})

            return redirect('/ngo/login')
    
    category_test_form = forms.TestForm()
    return render(request, 'ngo_category_test.html', {'form' : category_test_form, 'category' : "Toys"})

@jwt_required
def category_daily_use(request):
    
    if request.method == 'POST':
        category_test_form = forms.TestForm(request.POST, request.FILES)

        if category_test_form.is_valid():
            data = category_test_form.cleaned_data
            current_user_id = findCurrentUser(request)

            if current_user_id != None:
                print(current_user_id)
                ngo = models.NGO.objects.get(id=ObjectId(current_user_id))
                print(ngo.ngo_name)

                category = models.Global_Categories.objects(id=ObjectId('6893499515af1913e64d9648')).first()
                print(category.category_quantity)
                print(data['category_quantity'])
                if category.category_quantity < data['category_quantity']:
                    print("select a lower quantity")
                    return render(request, 'ngo_category_test.html', {'form' : category_test_form, 'error_message' : f"Please select a quantity less than {category.category_quantity + 1}"})

                ngo_cart = models.NGO_Cart(
                    category_name = "Daily_Use",
                    category_quantity = data['category_quantity']
                )

                ngo.ngo_cart.append(ngo_cart)

                ngo.save()

                print("Submitting the form ")
                return render(request, 'ngo_category_test.html', {'success_message' : "Request sent successfully, check your cart🛒"})

            return redirect('/ngo/login')
    
    category_test_form = forms.TestForm()
    return render(request, 'ngo_category_test.html', {'form' : category_test_form, 'category' : "Daily Use"})

@jwt_required
def category_stationary(request):
    
    if request.method == 'POST':
        category_test_form = forms.TestForm(request.POST, request.FILES)

        if category_test_form.is_valid():
            data = category_test_form.cleaned_data
            current_user_id = findCurrentUser(request)

            if current_user_id != None:
                print(current_user_id)
                ngo = models.NGO.objects.get(id=ObjectId(current_user_id))
                print(ngo.ngo_name)

                category = models.Global_Categories.objects(id=ObjectId('689349a015af1913e64d9649')).first()
                print(category.category_quantity)
                print(data['category_quantity'])
                if category.category_quantity < data['category_quantity']:
                    print("select a lower quantity")
                    return render(request, 'ngo_category_test.html', {'form' : category_test_form, 'error_message' : f"Please select a quantity less than {category.category_quantity + 1}"})

                ngo_cart = models.NGO_Cart(
                    category_name = "Stationary",
                    category_quantity = data['category_quantity']
                )

                ngo.ngo_cart.append(ngo_cart)

                ngo.save()

                print("Submitting the form ")
                return render(request, 'ngo_category_test.html', {'success_message' : "Request sent successfully, check your cart🛒"})

            return redirect('/ngo/login')
    
    category_test_form = forms.TestForm()
    return render(request, 'ngo_category_test.html', {'form' : category_test_form, 'category' : "Stationary"})


@jwt_required
def category_utensils(request):
    
    if request.method == 'POST':
        category_test_form = forms.TestForm(request.POST, request.FILES)

        if category_test_form.is_valid():
            data = category_test_form.cleaned_data
            current_user_id = findCurrentUser(request)

            if current_user_id != None:
                print(current_user_id)
                ngo = models.NGO.objects.get(id=ObjectId(current_user_id))
                print(ngo.ngo_name)

                category = models.Global_Categories.objects(id=ObjectId('689349a715af1913e64d964a')).first()
                print(category.category_quantity)
                print(data['category_quantity'])
                if category.category_quantity < data['category_quantity']:
                    print("select a lower quantity")
                    return render(request, 'ngo_category_test.html', {'form' : category_test_form, 'error_message' : f"Please select a quantity less than {category.category_quantity + 1}"})

                ngo_cart = models.NGO_Cart(
                    category_name = "Utensils",
                    category_quantity = data['category_quantity']
                )

                ngo.ngo_cart.append(ngo_cart)

                ngo.save()

                print("Submitting the form ")
                return render(request, 'ngo_category_test.html', {'success_message' : "Request sent successfully, check your cart🛒"})

            return redirect('/ngo/login')
    
    category_test_form = forms.TestForm()
    return render(request, 'ngo_category_test.html', {'form' : category_test_form, 'category' : "Utensils"})

@jwt_required
def ngo_cart(request):
    ngo_id = findCurrentUser(request)
    ngo = models.NGO.objects.get(id=ObjectId(ngo_id))
    total_quantity = sum(order.category_quantity for order in ngo.ngo_cart)
    return render(request, 'ngo_cart.html', {'ngo_cart' : ngo.ngo_cart, 'Total_Quantity': total_quantity })

@jwt_required
def ngo_order(request):
    ngo_id = findCurrentUser(request) 

    ngo = models.NGO.objects(id=ObjectId(ngo_id)).first()

    for order in ngo.ngo_cart:
        category = models.Global_Categories.objects(category_name = order.category_name).first() 
        category.category_quantity = category.category_quantity - order.category_quantity 
        category.save()

    ngo.ngo_cart = []

    ngo.save()

    return render(request, 'ngo_order_successful.html')

