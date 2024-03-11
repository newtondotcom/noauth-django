from db.models import *

def migrate_discord_users_to_noauth_users():
    noauth_users = NoAuthUsers.objects.all()
    for user in noauth_users:
        noauth_user.delete()
    discord_users = DiscordUsers.objects.all()
    for user in discord_users:
        noauth_user = NoAuthUsers(
            userID=user.userID,
            access_token=user.access_token,
            refresh_token=user.refresh_token,
            username=user.username,
            email=user.email,
            master=user.server_guild.master
        )
        noauth_user.save()
        user.delete()