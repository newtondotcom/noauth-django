from django.db import models
from django.contrib.auth.models import User

class DiscordServer(models.Model):
    guild_id = models.CharField(max_length=60)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    addip = models.CharField(max_length=40)
    client_secret = models.CharField(max_length=80)
    client_id = models.CharField(max_length=80)

class DiscordUsers(models.Model):
    userID = models.CharField(max_length=40, null=True, unique=True)
    access_token = models.CharField(max_length=300)
    refresh_token = models.CharField(max_length=300, null=True)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=150, null=True)  
    server_guild = models.ForeignKey(DiscordServer, on_delete=models.CASCADE, null=True)
    
class Payment(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField() # in days

class MyAuthUser(models.Model):
    userID = models.CharField(max_length=20)
    access_token = models.CharField(max_length=300)
    refresh_token = models.CharField(max_length=300, null=True)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=150, null=True) 

class MyServerMembers(models.Model):
    userID = models.CharField(max_length=20)

class ServerJoins(models.Model):
    userID = models.CharField(max_length=80)
    date = models.DateTimeField(auto_now_add=True)
    server = models.ForeignKey(DiscordServer, on_delete=models.CASCADE)