# File: forms.py
#
# This file contains the Django Form objects.

from django import forms

# form for the registration page
# fields are labeled as optional so that validation can be handled by the view
class RegistrationForm(forms.Form):
    username = forms.CharField(required=False)
    email = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(),
                                       required=False)
