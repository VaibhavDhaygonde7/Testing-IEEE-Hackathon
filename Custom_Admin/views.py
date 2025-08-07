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
