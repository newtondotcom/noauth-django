from django.contrib import admin
from .models import *

@admin.register(DiscordUsers)
class DiscordUsersAdmin(admin.ModelAdmin):
    list_display = ('userID', 'access_token', 'username')
    
    
@admin.register(DiscordServer)
class DiscordServerAdmin(admin.ModelAdmin):
    list_display = ('guild_id', 'owner')
    
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'date', 'duration')