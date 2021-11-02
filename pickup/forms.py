# File: forms.py
#
# This file contains the Django Form objects.
from django.forms import ModelForm
from .models import Parks, Player
from django import forms

# form for the registration page
# fields are labeled as optional so that validation can be handled by the view
class RegistrationForm(forms.Form):
    username = forms.CharField(required=False)
    email = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(),
                                       required=False)

# form for the edit profile page
class ProfileForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    date_of_birth = forms.DateField(required=False)
    gender = forms.ChoiceField(choices=Player.genders, required=False)
    height = forms.IntegerField(required=False)
    weight = forms.IntegerField(required=False)

#Creating the park form from the park model
class ParkForm(ModelForm):
    class Meta:
        model = Parks
        fields = ['name', 'street', 'city', 'state', 'zipcode']

