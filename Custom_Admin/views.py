from django.shortcuts import render, HttpResponse, redirect, Http404
from . import models
from bson import ObjectId
from mongoengine.connection import get_db
from gridfs import GridFS
# Create your views here.

def admin_verification(request):
    if request.method == 'POST': 
        print(request.POST.get('secret_code'))
        if request.POST.get('secret_code') == "hackathon":
            print("I'm here!")
            return redirect('/admin/home')
        return render(request, 'admin-verification.html', {'error_message' : 'Incorrect secret code'})

    return render(request, 'admin-verification.html')

def home(request):
    users = models.User.objects()
    return render(request, 'admin_home.html', {'users' : users})

def serve_photo(request, photo_id):
    try:
        db = get_db()  # gets the currently connected MongoEngine DB
        fs = GridFS(db)
        file = fs.get(ObjectId(photo_id))
        return HttpResponse(file.read(), content_type='image/jpeg')  # or detect content type dynamically
    except Exception as e:
        return HttpResponse(f"Error retrieving photo: {str(e)}", status=404)

def admin_approve(request):
    user = models.User.objects(id=ObjectId(request.GET.get('user_id'))).first()

    print(user)

    target_id = ObjectId(request.GET.get('photo_id'))

    for requests in user.user_donations:
        if requests.photo.grid_id == target_id:
            
            if requests.item == "Clothes":
                global_category = models.Global_Categories.objects(id=ObjectId('6893495615af1913e64d9644')).first()
            elif requests.item == "Medical Supplies":
                global_category = models.Global_Categories.objects(id=ObjectId('6893498515af1913e64d9646')).first()
            elif requests.item == "Toys":
                global_category = models.Global_Categories.objects(id=ObjectId('6893498b15af1913e64d9647')).first()
            elif requests.item == "Ration": 
                global_category = models.Global_Categories.objects(id=ObjectId('6893497a15af1913e64d9645')).first()
            elif requests.item == "Utensils": 
                global_category = models.Global_Categories.objects(id=ObjectId('689349a715af1913e64d964a')).first()
            elif requests.item == "Stationary":
                global_category = models.Global_Categories.objects(id=ObjectId('689349a015af1913e64d9649')).first()
            else:
                global_category = models.Global_Categories.objects(id=ObjectId('6893499515af1913e64d9648')).first()

            global_category.category_quantity = global_category.category_quantity + requests.quantity
            global_category.save()
            user.user_donations.remove(requests)
            user.save() 
            break 
    
    
    users = models.User.objects()
    return render(request, 'admin_home.html', {'users' : users})

def admin_reject(request):
    user = models.User.objects(id=ObjectId(request.GET.get('user_id'))).first()

    print(user)

    target_id = ObjectId(request.GET.get('photo_id'))

    for requests in user.user_donations:
        if requests.photo.grid_id == target_id:
            
            user.user_donations.remove(requests)
            user.save() 
            break 
    
    
    users = models.User.objects()
    return render(request, 'admin_home.html', {'users' : users})