from django.shortcuts import render
from django.urls import reverse
from django.core.validators import validate_email
from django.db.utils import IntegrityError
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.http import HttpResponse, HttpResponseRedirect, Http404


# Import models and forms
from .forms import ParkForm, RegistrationForm, ProfileForm, ScheduleForm, \
    ChangePasswordForm, SearchForm
from .models import Profile, Player, Parks, Schedule, FavoriteParks

def index(request):
    return render(request, "pickup/index.html")

def home(request):
    return render(request, 'pickup/home.html', {})
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
    return HttpResponseRedirect(reverse('edit_profile'))


# view for page to login to an existing account
class Login(LoginView):
    template_name = "pickup/login.html"


# view for logging out
class Logout(LogoutView):
    next_page = "login"


# view for changing one's password (must be logged in)
@login_required(login_url="login")
def change_password(request):
    # check for visiting for first time or submitting
    if request.method != "POST":
        return render(request, 'pickup/change_password.html', {})

    # get validated data
    input_form = ChangePasswordForm(request.POST)
    if not input_form.is_valid():
        return render(request, 'pickup/change_password.html',
                      {"error": "Error: Input is invalid."})

    input_data = input_form.cleaned_data

    # validate old password
    if authenticate(username=request.user.username,
                    password=input_data["old_password"]) == None:
        return render(request, 'pickup/change_password.html',
                      {"error": "Error: Incorrect old password."})

    # verify both passwords match
    if input_data["new_password"] != input_data["confirm_password"]:
        context = {"error":
                   "Error: New password does not match confirmed password."}
        return render(request, 'pickup/change_password.html', context)

    # update the user's password
    request.user.set_password(input_data["new_password"])
    request.user.save()
    login(request, request.user)
    return HttpResponseRedirect(reverse('view_profile'))


# view for page to view one's own profile (must be logged in)
@login_required(login_url="login")
def view_profile(request):
    return view_player(request, request.user.username)


# view for page to view any player's profile
@login_required(login_url="login")
def view_player(request, username):

    # check for viewing own profile
    is_self = request.user.username == username

    # get the user's information
    try:
        user = Player.objects.get(username=username)
    except Player.DoesNotExist:
        raise Http404

    # get the user's actual full name
    if user.first_name != "" and user.last_name != "":
        full_name = user.first_name + " " + user.last_name
    elif user.first_name != "" or user.last_name != "":
        full_name = user.first_name + user.last_name
    else:
        full_name = "Not provided"

    # get the user's age
    age = user.get_age()
    if age == None:
        age = "Not provided"

    # get the user's gender
    if user.gender != None:
        gender = Player.genders[user.gender][1]
    else:
        gender = "Not provided"

    # get the user's height
    if user.height != None:
        height = str(user.height) + " in"
    else:
        height = "Not provided"

    # get the user's weight
    if user.weight != None:
        weight = str(user.weight) + " lbs"
    else:
        weight = "Not provided"

    context = {"username": username,
               "full_name": full_name,
               "age": age,
               "gender": gender,
               "height": height,
               "weight": weight,
               "is_self": is_self,
               "is_public": user.is_public,}
    return render(request, 'pickup/profile.html', context)


# view for page to search for player profiles
@login_required(login_url="login")
def search_players(request):

    # check for visiting for first time or searching
    if "search_text" not in request.GET.keys():
        return render(request, 'pickup/search_players.html', {})

    # get validated data
    input_form = SearchForm(request.GET)
    input_form.is_valid()
    search_text = input_form.cleaned_data["search_text"]

    # get the list of players
    players = Player.objects.filter(username__contains=search_text)
    context = {"players": players,
               "search_input": search_text,
               "no_results": list(players) == [],
               "user": request.user,}
    return render(request, 'pickup/search_players.html', context)


def profile_list(request):
    profileList = Profile.objects.all()
    output = 'Name \t Weight \t Height \n'
    for q in profileList:
        output = output + '{Name} \t {Weight} \t {Height} \n'.format(Name=q.name, Weight=q.weight,
                                                                     Height=q.get_height_cust())
    return HttpResponse(output)

# view for page to view to edit one's profile (must be logged in)
@login_required(login_url="login")
def edit_profile(request):

    # get the user's information to prefill
    username = request.user.username
    user = Player.objects.get(username=username)

    # get gender options
    genders = [("", "<Select>")] + Player.genders

    # check for visiting for first time or submitting
    if request.method != "POST":

        # get date of birth if it already exists
        date_of_birth = ""
        if user.date_of_birth != None:
            date_of_birth = user.date_of_birth.strftime("%Y-%m-%d")

        context = {"genders": genders,
                   "username": username,
                   "first_name": user.first_name,
                   "last_name": user.last_name,
                   "date_of_birth": date_of_birth,
                   "gender": user.gender,
                   "height": user.height,
                   "weight": user.weight,
                   "is_public": user.is_public}
        return render(request, 'pickup/edit_profile.html', context)

    # get validated data
    input_form = ProfileForm(request.POST)

    if not input_form.is_valid():
        context = {"error": input_form.errors,
                   "genders": genders,
                   "username": username,
                   "first_name": request.POST["first_name"],
                   "last_name": request.POST["last_name"],
                   "date_of_birth": request.POST["date_of_birth"],
                   "gender": request.POST["gender"],
                   "height": request.POST["height"],
                   "weight": request.POST["weight"],
                   "is_public": request.POST["is_public"],}
        return render(request, 'pickup/edit_profile.html', context)

    input_data = input_form.cleaned_data

    # update the user's info
    user.first_name = input_data["first_name"]
    user.last_name = input_data["last_name"]
    user.date_of_birth = input_data["date_of_birth"]
    user.height = input_data["height"]
    user.weight = input_data["weight"]
    user.is_public = input_data["is_public"]

    # update gender
    if input_data["gender"] == "":
        user.gender = None
    else:
        user.gender = int(input_data["gender"])

    user.save()

    # redirect back to the profile page
    return HttpResponseRedirect(reverse('view_profile'))

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

                return render(request, reverse('Add Park'))

            return HttpResponse("Park has been added!")

    else:
        form = ParkForm()

    return render(request, 'pickup/add_park.html', {'form': form})

@login_required(login_url="login")
def view_park(request):
    # check for visiting for first time or submitting
    favorites = FavoriteParks.objects.filter(player=request.user).values("park_id")
    favoriteParks = Parks.objects.filter(id__in=favorites)

    # check for visiting for first time or searching
    if "search_text" not in request.GET.keys():

        return render(request, 'pickup/parks_list.html', {'favparks': favoriteParks})

    # get validated data
    input_form = SearchForm(request.GET)
    input_form.is_valid()
    search_text = input_form.cleaned_data["search_text"]

    # get the list of players
    favparks = Parks.objects.filter(name__contains=search_text, id__in=favorites)
    nofavparks = Parks.objects.filter(name__contains=search_text).exclude(id__in=favorites)
    context = {"favsearchparks": favparks,"nofavsearchparks": nofavparks,
               "search_input": search_text,'favparks': favoriteParks }
    return render(request, 'pickup/parks_list.html', context)

@login_required(login_url="login")
def park_signup(request, parkid):
    park = Parks.objects.get(id=parkid)
    error = None
    #Get the list of matches specific to this park
    try:
        matches = Schedule.objects.filter(park=parkid).order_by('date')
    except Schedule.DoesNotExist:
        matches = None

    if park:
        if request.method != 'POST':

            form = ScheduleForm()

            return render(request, 'pickup/schedule_time.html', {'form': form, 'park': park, 'matches': matches})

        form = ScheduleForm(request.POST)

        if not form.is_valid():
            context = {'form': form,
                       'park': park,
                       'error': form.errors,
                       'matches': matches}
            return render(request, 'pickup/schedule_time.html',context)

        input_data = form.cleaned_data

        #Save the new schedule
        current_player = request.user
        new_match = Schedule(player=current_player, park=park,time=input_data['time'], date=input_data['date'])
        try:
            new_match.save()
        except IntegrityError:
            error = "Error: Already signed up for this slot"

        context = {'form': form,
                   'park': park,
                   'matches': matches,
                   'error': error}
        return render(request, 'pickup/schedule_time.html', context)

    else:
        raise Http404

@login_required(login_url="login")
def favorite_park(request, add, parkid):
    park = Parks.objects.get(id=parkid)
    error = None
    #Get the list of matches specific to this park

    if park:
        if request.method != 'POST':

            return render(request, 'pickup/favorite_park.html', {'park': park, 'add': add})

        # Check if you are adding or deleting and respond
        current_player = request.user

        if add:
            try:
                new_fav = FavoriteParks(player=current_player, park=park)
                new_fav.save()
            except IntegrityError:
                error = "Error: This park is already one of your favorites!"
                return render(request, 'pickup/favorite_park.html', {'park': park, 'add': add, 'error':error})

        if not add:
            try:
                FavoriteParks.objects.get(park=park).delete()
            except IntegrityError:
                error = "Error: This park is not one of your favorites!"
                return render(request, 'pickup/favorite_park.html', {'park': park, 'add': add, 'error':error})

        return HttpResponseRedirect(reverse('parks'))

    else:
        raise Http404


@login_required(login_url="login")
def message_user(request):
    return render(request, 'pickup/messages.html')