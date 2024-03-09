from db.models import CurrentBots, Payment
from datetime import datetime, timedelta
from django.utils import timezone

def check_payments():
    current_date = timezone.now()
    bots = CurrentBots.objects.all()
    for bot in bots:
        if Payment.objects.filter(buyer=bot.bot, is_over=False, has_started=True).exists():
            payment = Payment.objects.filter(buyer=bot.bot, is_over=False, has_started=True).first()
            print(payment.start_date + timedelta(days=payment.duration) < current_date)
            if payment.start_date + timedelta(days=payment.duration) < current_date:
                payment.is_over = True
                payment.save()
                ## Check if there is another payment to start
                if Payment.objects.filter(buyer=bot.bot, is_over=False, has_started=False).exists():
                    payment_to_edit = Payment.objects.filter(buyer=bot.bot, is_over=False, has_started=False).first()
                    payment_to_edit.has_started = True
                    payment_to_edit.start_date = timezone.now()
                    payment_to_edit.save()
    ## Check if there is a bot without payment                
    for bot in bots:
        if not Payment.objects.filter(buyer=bot.bot, is_over=False, has_started=False).exists():
            CurrentBots.objects.filter(bot=bot.bot).delete()



def added_payment(id_buying):
    print("added_payment")
    payment = Payment.objects.get(id=id_buying)
    bot = payment.buyer
    payment_to_edit = None
    if Payment.objects.filter(buyer=bot, is_over=False, has_started=False).exists():
        payment_to_edit = Payment.objects.filter(buyer=bot, is_over=False, has_started=False).first()
        payment_to_edit.has_started = True
        payment_to_edit.start_date = timezone.now()
        payment_to_edit.save()
    if not CurrentBots.objects.filter(bot=bot).exists():
        #CurrentBots.objects.create(bot=bot)
        print("create")
