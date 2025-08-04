from django import forms

class RegisterForm(forms.Form):
    user_name = forms.CharField(required=True, max_length=100)
    user_email = forms.EmailField(required=True)
    user_phone_number = forms.CharField(required=True, max_length=10)
    user_password = forms.CharField(required=True, widget=forms.PasswordInput)



class LoginForm(forms.Form):
    user_email = forms.EmailField(required=True)
    user_password = forms.CharField(required=True, widget=forms.PasswordInput)