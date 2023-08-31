from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("isRegisteredAndActive/", isRegisteredAndActive), #check if a user is registered and active
    path("join/", join), #add a user to the server
    path("left/", left), #remove a user from the server
    path("checkToken/", checkToken), #check if a user's token is valid
    path("callback/", callback), #callback for oauth
    path("renewToken/", renew_token), #renew a user's token
    path("", index), #index page
    path('get_params/', get_params), #get the parameters for oauth
    path('get_ip_master/', get_ip_master), #get the ip of the master server
    path('get_members/', get_members), #get the members of a server
    path('update_webhook/', update_webhook), #update the webhook url for a server
    path('get_button/', get_button), #get the buttons for a server
    path('set_button_graphic/', set_button_graphic), #set the graphic for a button
    path('set_button_text/', set_button_text), #set the text for a button
    path('guild_joined/', guild_joined), #get the guilds a user has joined
    path('guild_left/', guild_left), #get the guilds a user has left
    path('set_role/', set_role), #set the role to give a user when they join
]

