import requests
from urllib.parse import urlencode
from db.models import *
from oauth.temp import *

def test_token(guild_id, user_id, access_token, refresh_token, constants):
    response = requests.get("https://discord.com/api/users/@me", headers={'Authorization': f"Bearer {access_token}"})
    if response.ok:
        print(f"user still valid for {user_id}")
        return
    else:
        try:
            new_access_token, new_refresh_token = renew_token(constants["clientId"], constants["clientSecret"], refresh_token)
            NoAuthUsers.objects.filter(userID=user_id, master=Bots.objects.filter(guild_id=guild_id)).update(access_token=new_access_token, refresh_token=new_refresh_token)
            print(f"Token updated for: {user_id}")
        except Exception as e:
            print(f"{user_id} is invalid, should be deleted" + str(e))
            master = Bots.objects.get(guild_id=guild_id)
            NoAuthUsers.objects.filter(userID=user_id, master=master).delete()

def renew_token(client_id, client_secret, refresh_token):
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post('https://discordapp.com/api/oauth2/token', data=urlencode(data), headers=headers)
    response.raise_for_status()
    data = response.json()
    return data['access_token'], data['refresh_token']