from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('profile/', views.profile_list, name='Profile List')
    path('register/', views.register, name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('profile/', views.view_profile, name='view_profile'),
    path('add_park/', views.add_park, name='Add Park'),
    path('profile/edit', views.edit_profile, name='edit_profile'),
    path("parks/", views.view_park, name='parks'),
    path("parks/<int:parkid>/", views.park_signup, name='park_signup'),
]
