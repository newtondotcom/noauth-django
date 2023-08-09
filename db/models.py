from django.db import models
from django.contrib.auth.models import User

class DiscordUsers(models.Model):
    userID = models.CharField(max_length=20)
    access_token = models.CharField(max_length=300)
    refresh_token = models.CharField(max_length=300, null=True)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=150, null=True)  
    linked_bot_public = models.CharField(max_length=300, null=True)
    server_guild_id = models.CharField(max_length=60, null=True)

class DiscordServer(models.Model):
    guild_id = models.CharField(max_length=60)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
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