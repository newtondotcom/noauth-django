from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("join/", join), #add a user to the server
    path("left/", left), #remove a user from the server
    path("verif/<str:key>/", verif), # 2nd callback for oauth
    path("renewToken/", renew_token), #renew a user's token
    path("", index), #index page
    path('get_params/', get_params), #get the parameters for oauth
    path('get_ip_master/', get_ip_master), #get the ip of the master server
    path('get_members/', get_members), #get the members of a server
    path('get_members_count/', get_members_count), #get the total members count of a bot
    path('get_members_per_server/', get_members_per_server), #get the members per server of a bot
    path('update_webhook/', update_webhook), #update the webhook url for a server
    path('get_button/', get_button), #get the buttons for a server
    path('set_button_graphic/', set_button_graphic), #set the graphic for a button
    path('set_button_text/', set_button_text), #set the text for a button
    path('set_button_content/', set_button_content), #set the content for a button
    path('guild_joined/', guild_joined), #get the guilds a user has joined
    path('guild_left/', guild_left), #get the guilds a user has left
    path('set_role/', set_role), #set the role to give a user when they join
    path('get_subscription/', get_subscription), #get the subscriptions for a user
    path('dl_user/', dl_user), #download a user's data
    path('add_whitelist/', add_whitelist), #add a user to the whitelist
    path('remove_whitelist/', rm_whitelist), #remove a user from the whitelist
    path('get_whitelist/', get_whitelist), #get the whitelist for a server
    path('update_access_token/', update_access_token), #update the access token for a user
    path('test_users/<str:bot>/', test_users), #test the users
    path('check_subscriptions/', check_subscription), #check the subscriptions
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

