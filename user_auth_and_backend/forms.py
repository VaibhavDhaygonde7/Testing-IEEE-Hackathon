from django import forms

class RegisterForm(forms.Form):
    user_name = forms.CharField(required=True, max_length=100)
    user_email = forms.EmailField(required=True)
    user_phone_number = forms.CharField(required=True, max_length=10)
    user_password = forms.CharField(required=True, widget=forms.PasswordInput)



class LoginForm(forms.Form):
    user_email = forms.EmailField(required=True)
    user_password = forms.CharField(required=True, widget=forms.PasswordInput)


class TestForm(forms.Form):
    quantity = forms.IntegerField(
        label="Quantity",
        min_value=1,
        widget=forms.NumberInput(attrs={'class' : 'form-control'})
    )

    DROP_OFF_LOCATIONS = [
        ('pune', 'Pune'),
        ('mumbai', 'Mumbai'),
        ('delhi', 'Delhi'),
    ]

    drop_off_location = forms.ChoiceField(
        label='Drop-off Location: ',
        choices=DROP_OFF_LOCATIONS,
        widget=forms.Select(attrs={'class':'form-control'})
    )

    photo = forms.ImageField(
        label="Upload Photo of the item",
        required=True,  # Set True if the photo is mandatory
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    date = forms.DateField(
        label="Date: ",
        widget=forms.DateInput(attrs={'type':'date', 'class':'form-control'})
    )
