from django.shortcuts import render

from django.http import HttpResponse
from .models import Profile


def index(request):
    return HttpResponse("Hello World. This is my test of creating a view")

# view for page to register a new account
def register(request):
    return render(request, 'pickup/register.html', {})

# view for creating an account
# reached by an action from the register page
def create_account(request):

    # verify no fields are empty
    if (request.POST["username"] == "" or request.POST["email"] == "" or
        request.POST["password"] == "" or
        request.POST["confirm_password"] == ""):

        context = {"username": request.POST["username"],
                   "email": request.POST["email"],
                   "error": "Error: All fields are required.",}
        return render(request, 'pickup/register.html', context)

    # verify the '@' and '.' symbols appear in the email
    if ('@' not in request.POST["email"] or '.' not in request.POST["email"]):
        context = {"username": request.POST["username"],
                   "error": "Error: Invalid email address.",}
        return render(request, 'pickup/register.html', context)

    # verify passwords match
    if (request.POST["password"] != request.POST["confirm_password"]):
        context = {"username": request.POST["username"],
                   "email": request.POST["email"],
                   "error": "Error: Passwords do not match.",}
        return render(request, 'pickup/register.html', context)

    return HttpResponse("Success!")

def profile_list(request):
    profileList = Profile.objects.all()
    output = 'Name \t Weight \t Height \n'
    for q in profileList:
        output = output + '{Name} \t {Weight} \t {Height} \n'.format(Name=q.name, Weight=q.weight,
                                                                     Height=q.get_height_cust())
    return HttpResponse(output)

