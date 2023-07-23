from django.contrib import admin
from .models import *

@admin.register(DiscordUsers)
class DiscordUsersAdmin(admin.ModelAdmin):
    list_display = ('userID', 'access_token', 'username')