from django import forms

class NGORegistrationForm(forms.Form):
    ngo_name = forms.CharField(required=True, max_length=100)
    ngo_email = forms.EmailField(required=True)
    ngo_password = forms.CharField(required=True, widget=forms.PasswordInput)
    ngo_phone_number = forms.CharField(required=10, max_length=10)
    ngo_address = forms.CharField(required=True)

class NGOLogin(forms.Form):
    ngo_email = forms.EmailField(required=True)
    ngo_password = forms.CharField(required=True, widget=forms.PasswordInput)

class TestForm(forms.Form):
    category_quantity = forms.IntegerField(required=True, min_value=1)