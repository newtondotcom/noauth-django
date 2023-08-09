from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", register), #register a user of our oauth
    path("isRegisteredAndActive/", isRegisteredAndActive), #check if a user is registered and active
    path("addServerMember/", addServerMember), #add a user to our server
    path("removeServerMember/", removeServerMember), #remove a user from our server
]
