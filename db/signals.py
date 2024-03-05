from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from db.models import *

# Define your function to execute when a row is added
@receiver(post_save, sender=CurrentBots)
def handle_row_added(sender, instance, created, **kwargs):
    if created:
        # Code to execute when a row is added
        print("A row was added to MyModel")

# Define your function to execute when a row is deleted
@receiver(post_delete, sender=CurrentBots)
def handle_row_deleted(sender, instance, **kwargs):
    # Code to execute when a row is deleted
    print("A row was deleted from MyModel") 

@receiver(post_save, sender=Payment)
def handle_payment_added(sender, instance, created, **kwargs):
    if created:
        payment = Payment.objects.get(id=instance.id)
        buyer = payment.buyer
        if not CurrentBots.objects.filter(bot=buyer).exists():
            CurrentBots.objects.create(bot=buyer)