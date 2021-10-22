from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Profile
from .forms import ParkForm


def index(request):
    return HttpResponse("Hello World. This is my test of creating a view")


def profile_list(request):
    profileList = Profile.objects.all()
    output = 'Name \t Weight \t Height \n'
    for q in profileList:
        output = output + '{Name} \t {Weight} \t {Height} \n'.format(Name=q.name, Weight=q.weight,
                                                                     Height=q.get_height_cust())
    return HttpResponse(output)


def add_park(request):
    if request.method == 'POST':
        form = ParkForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['parkName'])

            return HttpResponseRedirect('/thanks/')

    else:
        form = ParkForm()

    return render(request, 'add_park.html', {'form': form})
