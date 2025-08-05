from mongoengine import connect, StringField, EmailField, Document
from bson import ObjectId


class User(Document):
    user_name = StringField(required=True, max_length=100)
    user_email = EmailField(required=True)
    user_password = StringField(required=True)
    user_phone_number = StringField(max_length=10)
    


try:
    connect(
        db='DB', 
        host='mongodb+srv://vaibhavdhaygonde:vaibhavpassword@startingagain.huaz1db.mongodb.net/?retryWrites=true&w=majority&appName=StartingAgain'
    )

    user = User.objects.get(id=ObjectId('6890afe0ed3844ea37442f18'))
    print(user.user_name)


except Exception as e: 
    print(e) 