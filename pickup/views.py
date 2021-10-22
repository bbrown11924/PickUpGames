from django.shortcuts import render
from django.urls import reverse
from django.core.validators import validate_email
from django.db.utils import IntegrityError
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseRedirect

# Import models and forms
from .forms import ParkForm, RegistrationForm
from .models import Profile, Player, Parks


def index(request):
    return HttpResponse("Hello World. This is my test of creating a view")


# view for page to register a new account
def register(request):
    # check for visiting for first time or submitting
    if request.method != "POST":
        return render(request, 'pickup/register.html', {})

    # get validated data
    input_form = RegistrationForm(request.POST)
    input_form.is_valid()
    input_data = input_form.cleaned_data

    # verify no fields are empty
    if (input_data["username"] == "" or input_data["email"] == "" or
            input_data["password"] == "" or input_data["confirm_password"] == ""):
        context = {"username": input_data["username"],
                   "email": input_data["email"],
                   "error": "Error: All fields are required.", }
        return render(request, 'pickup/register.html', context)

    # verify the email address is properly formatted
    try:
        validate_email(input_data["email"])
    except:
        context = {"username": input_data["username"],
                   "error": "Error: Invalid email address.", }
        return render(request, 'pickup/register.html', context)

    # verify passwords match
    if input_data["password"] != input_data["confirm_password"]:
        context = {"username": input_data["username"],
                   "email": input_data["email"],
                   "error": "Error: Passwords do not match.", }
        return render(request, 'pickup/register.html', context)

    # is valid: add the user to the Player database
    try:
        new_player = Player.objects.create_user(input_data["username"],
                                                input_data["email"],
                                                input_data["password"])
    except IntegrityError:
        context = {"email": input_data["email"],
                   "error": "Error: User name unavailable.", }
        return render(request, 'pickup/register.html', context)

    # log the user in and send them to the profile page
    login(request, new_player)
    return HttpResponseRedirect(reverse('view_profile'))


# view for page to login to an existing account
class Login(LoginView):
    template_name = "pickup/login.html"
    next = "profile"


# view for logging out
class Logout(LogoutView):
    next_page = "login"


# view for page to view a profile (must be logged in)
@login_required(login_url="login")
def view_profile(request):
    return render(request, 'pickup/profile.html', {})


def profile_list(request):
    profileList = Profile.objects.all()
    output = 'Name \t Weight \t Height \n'
    for q in profileList:
        output = output + '{Name} \t {Weight} \t {Height} \n'.format(Name=q.name, Weight=q.weight,
                                                                     Height=q.get_height_cust())
    return HttpResponse(output)

@login_required(login_url="login")
def add_park(request):
    if request.method == 'POST':
        form = ParkForm(request.POST)
        if form.is_valid():
            input_data = form.cleaned_data
            # is valid: add the user to the Player database
            try:
                current_player = request.user

                new_park = Parks(player=current_player, name=input_data['name'],
                                 street=input_data['street'], city=input_data['city'],
                                 state=input_data['state'], zipcode=input_data['zipcode'])
                new_park.save()

            except IntegrityError:

                return render(request, 'pickup/add_park.html')

            return HttpResponse("Park has been added!")

    else:
        form = ParkForm()

    return render(request, 'add_park.html', {'form': form})
