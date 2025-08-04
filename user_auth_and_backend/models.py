from django.db import models
from mongoengine import Document, StringField, EmailField

# Create your models here.
class User(Document):
    user_name = StringField(required=True, max_length=100)
    user_email = EmailField(required=True)
    user_password = StringField(required=True)
    user_phone_number = StringField(max_length=10)
    
