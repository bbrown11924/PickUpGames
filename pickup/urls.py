from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile_list, name='Profile List'),
    path('add_park/', views.add_park, name='Add Park')
]