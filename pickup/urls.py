from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('profile/', views.view_profile, name='view_profile'),
    path('player/<str:username>/', views.view_player, name='view_player'),
    path('searchplayers/', views.search_players, name='search_players'),
    path('changepassword/', views.change_password, name='change_password'),
    path('add_park/', views.add_park, name='Add Park'),
    path('profile/edit', views.edit_profile, name='edit_profile'),
    path("parks/", views.view_park, name='parks'),
    path("parks/<int:parkid>/", views.event_signup, name='event_signup'),
    path("favorite/<int:add>/<int:parkid>/", views.favorite_park, name='favorite_park'),
    path("parks/<int:parkid>/<int:add>/<int:eventid>/", views.join_event, name='join_event'),
    path('messages/', views.message_user, name="messages"),
    path('messages/<str:username>', views.message_conversation, name="messages"),
    path('newMessage/', views.new_message, name= 'new_message'),
]
