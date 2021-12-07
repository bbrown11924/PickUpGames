from django.contrib import admin

from .models import Profile, Player, Parks, Schedule, FavoriteParks, \
    EventSignup, Messages

# Register your models here.
admin.site.register(Profile)
admin.site.register(Player)
admin.site.register(Parks)
admin.site.register(Schedule)
admin.site.register(FavoriteParks)
admin.site.register(EventSignup)
admin.site.register(Messages)
