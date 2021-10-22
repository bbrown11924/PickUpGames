from django.forms import ModelForm
from .models import Parks
from localflavor.us.forms import USStateSelect, USZipCodeField

class ParkForm(ModelForm):
    class Meta:
        model = Parks
        fields = ['name','street', 'city', 'state', 'zipcode']


