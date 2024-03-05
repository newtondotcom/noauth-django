from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from db.models import *
from oauth.docker import *
from oauth.subscriptions import *

# Define your function to execute when a row is added
@receiver(post_save, sender=CurrentBots)
def handle_row_added(sender, instance, created, **kwargs):
    if created:
        fetch_docker_master()

# Define your function to execute when a row is deleted
@receiver(post_delete, sender=CurrentBots)
def handle_row_deleted(sender, instance, **kwargs):
    fetch_docker_master()

@receiver(post_save, sender=Payment)
def handle_row_added(sender, instance, created, **kwargs):
    if created:
        added_payment(instance.id)