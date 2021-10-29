import datetime
from dateutil.relativedelta import relativedelta

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# model for a player, containing their user/login data as well as information
# in their profile
class Player(User):
    date_of_birth = models.DateField(null=True, blank=True)
    
    # set constants for gender values
    MALE = 0
    FEMALE = 1
    OTHER = 2
    gender = models.IntegerField(null=True, blank=True,
                                 choices=[(MALE, "Male"), (FEMALE, "Female"),
                                          (OTHER, "Other")])

    height = models.IntegerField(null=True, blank=True) # in inches
    weight = models.IntegerField(null=True, blank=True) # in pounds

    # return the user's age based on their birthday, None if no birthday was
    # provided
    def get_age(self):
        if self.date_of_birth == None:
            return None
        return relativedelta(timezone.now(), self.date_of_birth).years

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


