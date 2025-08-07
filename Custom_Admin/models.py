from django.db import models
from mongoengine import EmbeddedDocument, Document, StringField, IntField, DateField, FileField, EmailField, ListField, EmbeddedDocumentField

# Create your models here.


class User_Donation(EmbeddedDocument):
    quantity = IntField(required=True, min_value=1)
    drop_off_location = StringField(required=True, choices=['pune', 'mumbai', 'delhi'])
    date = DateField(required=True)
    photo = FileField(required=True)
    item = StringField(default="Test_item")

class User(Document):
    user_name = StringField(required=True, max_length=100)
    user_email = EmailField(required=True)
    user_password = StringField(required=True)
    user_phone_number = StringField(max_length=10)
    user_donations = ListField(EmbeddedDocumentField(User_Donation), default=[])   