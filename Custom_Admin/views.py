from django.shortcuts import render, HttpResponse, redirect, Http404
from . import models
from bson import ObjectId
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


def serve_photo(request, user_id, file_id):
    user = models.User.objects(id=ObjectId(user_id))
    for donation_photos in user.user_donations:
        if donation_photos.photo == ObjectId(file_id):
            content_type = donation_photos.photo.content_type or "image/jpeg"    
            return HttpResponse(donation_photos.photo.read(), content_type=content_type)

    return HttpResponse("Not found")    