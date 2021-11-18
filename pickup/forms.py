# File: forms.py
#
import datetime

# This file contains the Django Form objects.
from django.forms import ModelForm
from .models import Parks, Player, Schedule
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
    is_public = forms.BooleanField(required=False)

# form for the change password page
# fields are labeled as optional so that validation can be handled by the view
class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(),
                                       required=False)

#Creating the park form from the park model
class ParkForm(ModelForm):
    class Meta:
        model = Parks
        fields = ['name', 'street', 'city', 'state', 'zipcode']

class DateInput(forms.DateInput):
    input_type = 'date'

#Creating the park form from the park model
class ScheduleForm(ModelForm):
    class Meta:
        model = Schedule
        fields = ['date', 'time']
        widgets = {
            'date': DateInput()
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return date

# form for searching something
class SearchForm(forms.Form):
    search_text = forms.CharField(required=False)

class NewMessageForm(forms.Form):
    receiver = forms.CharField(required=True)
    userMessage = forms.CharField(max_length=1000, required=True)

