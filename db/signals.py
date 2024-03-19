from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from db.models import *
from oauth.docker import *
from oauth.subscriptions import *
from django.db.models import F

@receiver(post_save, sender=CurrentBots)
def handle_row_added(sender, instance, created, **kwargs):
    if created:
        add_bot(instance)

@receiver(post_delete, sender=CurrentBots)
def handle_row_deleted(sender, instance, **kwargs):
    remove_bot(instance)

@receiver(post_save, sender=Payment)
def handle_row_added(sender, instance, created, **kwargs):
    if created:
        added_payment(instance.id)

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