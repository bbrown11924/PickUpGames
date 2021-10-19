from django.db import models


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


