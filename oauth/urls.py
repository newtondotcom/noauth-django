from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("isRegisteredAndActive/", isRegisteredAndActive), #check if a user is registered and active
    path("join/", join), #add a user to the server
    path("checkToken/", checkToken), #check if a user's token is valid
    path("callback/", callback), #callback for oauth
    path("renewToken/", renew_token), #renew a user's token
]

