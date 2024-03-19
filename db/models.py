from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

## Discord Servers registered
class Bots(models.Model):
    guild_id = models.CharField(max_length=60)
    owner_discord_id = models.CharField(max_length=40, null=True)
    addip = models.CharField(max_length=40)
    client_secret = models.CharField(max_length=80)
    client_id = models.CharField(max_length=80)
    webhook_url = models.CharField(max_length=200, null=True,default="https://discord.com/api/webhooks/1193146552907202680/hRpr4dL9HpJGVcPhHBPa-cF4I2pFzqq0HWgZv8GiOxxysTrvCnuLABlEsl2luEe_YZcb")
    color = models.IntegerField(default=3447003, null=True)
    name = models.CharField(max_length=50, null=True)
    token = models.CharField(max_length=300, null=True)
    speed = models.IntegerField(default=7, null=True)

    def __str__(self):
        return self.name
    
class DiscordServerJoined(models.Model):
    master = models.ForeignKey(Bots, on_delete=models.CASCADE)
    guild_id = models.CharField(max_length=60)
    roleToGiveVerif = models.CharField(max_length=60, null=True)
    
class NoAuthUsers(models.Model):
    userID = models.CharField(max_length=40, null=True)
    access_token = models.CharField(max_length=300)
    refresh_token = models.CharField(max_length=300, null=True)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=150, null=True)  
    master = models.ForeignKey(Bots, on_delete=models.CASCADE, null=True, blank=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
## Discord Users joined
class UsersJoinServer(models.Model):
    userID = models.CharField(max_length=80)
    date = models.DateTimeField(auto_now_add=True)
    server = models.ForeignKey(DiscordServerJoined, on_delete=models.CASCADE)
    has_joined = models.BooleanField(default=False)

## Payments
class Payment(models.Model):
    buyer = models.ForeignKey(Bots, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField() # in days
    is_over = models.BooleanField(default=False)
    has_started = models.BooleanField(default=False, null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)

# Button models
class Button(models.Model):
    image = models.CharField(max_length=2000, null=True, blank=True)
    color = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    footer = models.CharField(max_length=50, null=True, blank=True)
    server = models.ForeignKey(DiscordServerJoined, on_delete=models.CASCADE, null=True, blank=True)
    content = models.CharField(max_length=2000, null=True, blank=True, default="Authentificate here !")

    def __str__(self):
        return self.name
    
class Whitelist(models.Model):
    server = models.ForeignKey(Bots, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=40)
    added_by = models.CharField(max_length=40)
    date = models.DateTimeField(auto_now_add=True)

class CurrentBots(models.Model):
    bot = models.ForeignKey(Bots, on_delete=models.CASCADE)

    def __str__(self):
        return self.bot.name
    
class Counters(models.Model):
    name = models.CharField(max_length=40, null=True, blank=True)
    count = models.IntegerField(default=0)
    master = models.ForeignKey(Bots, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
class WlRules(models.Model):
    joinlimit = models.IntegerField(default=0)
    sessionlimit = models.IntegerField(default=0)
    whitelist = models.ForeignKey(Whitelist, on_delete=models.CASCADE, null=True, blank=True)