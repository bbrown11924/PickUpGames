from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('profile/', views.view_profile, name='view_profile'),
]