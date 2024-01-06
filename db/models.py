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

    def __str__(self):
        return self.name
    
class DiscordServerJoined(models.Model):
    master = models.ForeignKey(Bots, on_delete=models.CASCADE)
    guild_id = models.CharField(max_length=60)
    roleToGiveVerif = models.CharField(max_length=60, null=True)
    
@receiver(post_save, sender=Bots)
def create_button_and_server_joined(sender, instance, created, **kwargs):
    if created:
        
        # Create a DiscordServerJoined instance
        serv = DiscordServerJoined.objects.create(
            master=instance, 
            guild_id=instance.guild_id
        )

        # Create a Button instance
        Button.objects.create(
            server=serv,
            image="https://i.imgur.com/AfFp7pu.png",
            color=167772,  
            name="Name",
            title="Title",
            description="Description",
            footer="Footer",
            content="Authentificate here !"
        )


## Discord Users registered
class DiscordUsers(models.Model):
    userID = models.CharField(max_length=40, null=True, unique=True)
    access_token = models.CharField(max_length=300)
    refresh_token = models.CharField(max_length=300, null=True)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=150, null=True)  
    server_guild = models.ForeignKey(DiscordServerJoined, on_delete=models.CASCADE, null=True, blank=True)

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