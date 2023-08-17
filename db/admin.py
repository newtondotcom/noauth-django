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

@admin.register(MyServerMembers)
class MyServerMembersAdmin(admin.ModelAdmin):
    list_display = ('userID',)

@admin.register(MyAuthUser)
class MyAuthUserAdmin(admin.ModelAdmin):
    list_display = ('userID', 'username')

@admin.register(ServerJoins)
class ServerJoinsAdmin(admin.ModelAdmin):
    list_display = ('userID', 'date', 'server', 'has_joined')