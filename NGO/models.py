from django.db import models
from mongoengine import Document, EmailField, StringField, IntField, EmbeddedDocument, EmbeddedDocumentField, ListField

# Create your models here.


class NGO_Cart(EmbeddedDocument):
    category_name = StringField(required=True)
    category_quantity = IntField(required=True, min_value=1)


class NGO(Document):
    ngo_name = StringField(required=True, max_length=100)
    ngo_email = EmailField(required=True)
    ngo_password = StringField(required=True)
    ngo_phone_number = StringField(max_length=10)
    ngo_address = StringField(required=True)

    ngo_cart = ListField(EmbeddedDocumentField(NGO_Cart), default=[])

    meta = {'collection' : 'ngo'}


class Global_Categories(Document):
    category_name = StringField(required=True, max_length=100)
    category_quantity = IntField(required=True,default=0, min_value=0)
    meta = {'collection' : 'global_categories'}