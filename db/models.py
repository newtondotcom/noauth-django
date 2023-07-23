from django.db import models
from django.contrib.auth.models import User

class DiscordUsers(models.Model):
    userID = models.CharField(max_length=20)
    access_token = models.CharField(max_length=300)
    refresh_token = models.CharField(max_length=300, null=True)
    username = models.CharField(max_length=50)
    linked_bot_public = models.CharField(max_length=300, null=True)
    server_guild_id = models.CharField(max_length=60, null=True)

class DiscordServer(models.Model):
    guild_id = models.CharField(max_length=60)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
