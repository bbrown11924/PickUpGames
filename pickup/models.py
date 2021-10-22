from django.db import models
from localflavor.us.models import USStateField, USZipCodeField
from localflavor.us.us_states import STATE_CHOICES

# Create your models here.
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
    name = models.CharField(max_length=200)
    # address must be inserted after formatting with the googlemaps package
    street = models.CharField(max_length=400)
    city = models.CharField(max_length=400)
    state = USStateField(choices=STATE_CHOICES)
    zipcode = USZipCodeField()
    # Overload the query print
    def __str__(self):
        return self.name
