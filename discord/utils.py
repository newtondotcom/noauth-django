import discord
import requests
import os

API_BASE_URL = os.environ.get('API_BASE_URL', 'https://discordapp.com/api')


BOT_TOKEN = 'MTEzMjY4MTg1MDUyODIwMjc4Mg.GnYENS.GfLGZeMMX8vsVEOdVgnqqkwlw4YXjqbivD5-UA'

        
def find_user_in_guild(guild, user_id_str):
    user_id = int(user_id_str)
    for member in guild.members:
        if member.id == user_id:
            return True
    return False

def add_to_guild(access_token, userID, guildID):
    url = f"{API_BASE_URL}/guilds/{guildID}/members/{userID}"
    data = {
        "access_token" : access_token,
    }
    headers = {
        "Authorization" : f"Bot {BOT_TOKEN}",
        'Content-Type': 'application/json'
    }
    response = requests.put(url=url, headers=headers, json=data)
    print(response.status_code)
