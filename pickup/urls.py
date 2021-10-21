from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile_list, name='Profile List'),
    path('register/', views.register, name='register'),
    path('create_account/', views.create_account, name='create_account'),
]