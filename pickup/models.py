import datetime
from dateutil.relativedelta import relativedelta

from django.db import models
from localflavor.us.models import USStateField, USZipCodeField
from localflavor.us.us_states import STATE_CHOICES
from django.contrib.auth.models import User


# model for a player, containing their user/login data as well as information
# in their profile
class Player(User):
    date_of_birth = models.DateField(null=True, blank=True)

    # set constants for gender values
    MALE = 0
    FEMALE = 1
    OTHER = 2
    genders = [(MALE, "Male"), (FEMALE, "Female"), (OTHER, "Other")]
    gender = models.IntegerField(null=True, blank=True, choices=genders)

    height = models.IntegerField(null=True, blank=True) # in inches
    weight = models.IntegerField(null=True, blank=True) # in pounds

    # return the user's age based on their birthday, None if no birthday was
    # provided
    def get_age(self):
        if self.date_of_birth == None:
            return None
        return relativedelta(datetime.date.today(), self.date_of_birth).years

class Messages(models.Model):
    sender = models.ForeignKey(Player, related_name="sender", on_delete=models.RESTRICT)
    receiver = models.ForeignKey(Player, related_name="receiver", on_delete=models.RESTRICT)
    message = models.CharField(max_length=1000)


class Profile(models.Model):
    name = models.CharField(max_length=200)
    weight = models.IntegerField()
    height = models.IntegerField()

    def __str__(self):
        return self.name

    def get_height_cust(self):
        inches = self.height % 12
        feet = (self.height - inches) // 12
        return "{feet}\'{inches}\"".format(feet=feet, inches=inches)


# Create your models here.
class Courts(models.Model):
    name = models.CharField(max_length=200)
    # Will be obtained with the google maps api
    latitude = models.FloatField()
    longitude = models.FloatField()
    park = models.ForeignKey('pickup.Parks', on_delete=models.CASCADE)

    # Overload the query print
    def __str__(self):
        return self.name

# Create your models here.
class Parks(models.Model):
    class Meta:
        # Prevent the same park from being entered twice
        constraints = [
            models.UniqueConstraint(fields=['name', 'street', 'city', 'state', 'zipcode'], name="%(app_label)s_%("
                                                                                                "class)s_unique")
        ]

    player = models.ForeignKey(User, default="", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    # address will be inserted after formatting with the googlemaps package
    street = models.CharField(max_length=400)
    city = models.CharField(max_length=400)
    state = USStateField(choices=STATE_CHOICES)
    zipcode = USZipCodeField()

    objects = models.Manager()

    # Overload the query print
    def __str__(self):
        return self.name

class Schedule(models.Model):
    class Meta:
        # Prevent the same park from being entered twice
        constraints = [
            models.UniqueConstraint(fields=['player', 'park', 'time', 'date'], name="%(app_label)s_%(class)s_unique")]

    times = []
    for i in range(0, 24 * 4):
        time = datetime.datetime(1900, 1, 1, 0, 0) + datetime.timedelta(minutes=15 * i)
        datetext = time.strftime("%I:%M %p")
        times.append((i, datetext))

    player = models.ForeignKey(User, default="", on_delete=models.CASCADE)
    park = models.ForeignKey(Parks, default="", on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    time = models.IntegerField(choices=times)

    objects = models.Manager()

