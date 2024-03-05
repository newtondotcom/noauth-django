from db.models import *
from datetime import datetime

def check_payments():
    date = datetime.datetime.now()
    bots = CurrentBots.objects.all()
    for bot in bots:
        payments = Payment.objects.filter(buyer=bot.bot, is_over=False)
        for payment in payments:
            if  payment.date + datetime.timedelta(days=payment.duration) < date:
                payment.is_over = True
                payment.save()
        if not Payment.objects.filter(buyer=bot.bot, is_over=False).exists():
            CurrentBots.objects.filter(bot=bot.bot).delete()

def added_payment(id_buying):
    payment = Payment.objects.get(id=id_buying)
    bot = payment.buyer
    if not CurrentBots.objects.filter(bot=bot).exists():
        CurrentBots.objects.create(bot=bot)