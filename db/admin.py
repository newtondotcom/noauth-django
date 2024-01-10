from django.contrib import admin
from .models import *

@admin.register(DiscordUsers)
class DiscordUsersAdmin(admin.ModelAdmin):
    list_display = ('username','server_guild')
    
@admin.register(Bots)
class DiscordServerAdmin(admin.ModelAdmin):
    list_display = ('guild_id', 'owner_discord_id')
    search_fields = ('guild_id', 'owner_discord_id')
    
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'date', 'duration')

@admin.register(UsersJoinServer)
class UsersJoinServerAdmin(admin.ModelAdmin):
    list_display = ('userID', 'date', 'server', 'has_joined')

@admin.register(Button)
class ButtonAdmin(admin.ModelAdmin):
    list_display = ('server', 'image', 'color', 'name', 'title', 'description', 'footer')
    
@admin.register(DiscordServerJoined)
class DiscordServerJoinedAdmin(admin.ModelAdmin):
    list_display = ('master', 'guild_id')

@admin.register(Whitelist)
class WhitelistAdmin(admin.ModelAdmin):
    list_display = ('server', 'user_id')