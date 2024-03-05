from db.models import CurrentBots, Payment
from datetime import datetime, timedelta
from django.utils import timezone

def check_payments():
    current_date = timezone.now()
    bots = CurrentBots.objects.all()
    for bot in bots:
        payments = Payment.objects.filter(buyer=bot.bot, is_over=False)
        for payment in payments:
            if payment.date + timedelta(days=payment.duration) < current_date:
                payment.is_over = True
                payment.save()
        if not Payment.objects.filter(buyer=bot.bot, is_over=False).exists():
            CurrentBots.objects.filter(bot=bot.bot).delete()

def added_payment(id_buying):
    payment = Payment.objects.get(id=id_buying)
    bot = payment.buyer
    if not CurrentBots.objects.filter(bot=bot).exists():
        CurrentBots.objects.create(bot=bot)
