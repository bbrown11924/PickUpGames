from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Profile
from django.shortcuts import render


def home(request):
    return render(request, 'pickup/home.html', {})


def profile_list(request):
    profileList = Profile.objects.all()
    output = 'Name \t Weight \t Height \n'
    for q in profileList:
        output = output + '{Name} \t {Weight} \t {Height} \n'.format(Name=q.name, Weight=q.weight,
                                                                     Height=q.get_height_cust())
    return HttpResponse(output)

