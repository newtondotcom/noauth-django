from django.contrib import admin
from .models import *
    
@admin.register(Bots)
class DiscordServerAdmin(admin.ModelAdmin):
    list_display = ('name','user_verified')
    search_fields = ('guild_id', 'owner_discord_id')

    def user_verified(self, obj):
        return NoAuthUsers.objects.filter(master=obj).count()
    
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'date', 'duration')

@admin.register(UsersJoinServer)
class UsersJoinServerAdmin(admin.ModelAdmin):
    list_display = ('userID', 'date', 'server', 'has_joined')

@admin.register(Button)
class ButtonAdmin(admin.ModelAdmin):
    list_display = ('server', 'name')
    
@admin.register(DiscordServerJoined)
class DiscordServerJoinedAdmin(admin.ModelAdmin):
    list_display = ('master', 'guild_id')

@admin.register(Whitelist)
class WhitelistAdmin(admin.ModelAdmin):
    list_display = ('server', 'user_id')

@admin.register(NoAuthUsers)
class NoAuthUsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'master')

@admin.register(CurrentBots)
class CurrentBotsAdmin(admin.ModelAdmin):
    list_display = ('bot',)

@admin.register(WlRules)
class WlRulesAdmin(admin.ModelAdmin):
    list_display = ('joinlimit', 'sessionlimit','whitelist')