from django.db import models
from django.contrib.auth.models import User

class Player(User):
    pass

class Messages(models.Model):
    sender = models.ForeignKey(User, related_name = "sender", on_delete=models.RESTRICT)
    reciever = models.ForeignKey(User, related_name="reciever", on_delete=models.RESTRICT)
    message = models.CharField(max_length= 1000)


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


