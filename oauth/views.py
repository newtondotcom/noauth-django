from db.models import *
import os
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import requests
import json
from dotenv import load_dotenv
load_dotenv()

def callback(request):
    code = request.args.get('code')

    form_data = {
        'client_id': os.get_environ('OAUTH2_CLIENT_ID'),
        'client_secret': os.get_environ('OAUTH2_CLIENT_SECRET'),
        'grant_type': 'authorization_code',
        'redirect_uri': os.get_environ('OAUTH2_REDIRECT_URI'),
        'scope': os.get_environ('OAUTH2_CLIENT_ID'),
        'code': code
    }

    try:
        token_response = requests.post('https://discordapp.com/api/oauth2/token', data=form_data, headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        token_data = token_response.json()
        access_token = token_data['access_token']
        refresh_token = token_data['refresh_token']
        headers_with_token = {'Authorization': f'{token_data["token_type"]} {access_token}'}
        user_data_response = requests.get('https://discordapp.com/api/users/@me', headers=headers_with_token)
        user_data = user_data_response.json()

        user_id = user_data['id']
        with open('./object.json', 'r') as file:
            object_json = json.load(file)

        if any(user['userID'] == user_id for user in object_json):
            print(f'[-] {user_data["username"]}#{user_data["discriminator"]}')
        else:
            print(f'[+] {user_data["username"]}#{user_data["discriminator"]}')
            avatar_url = f'https://cdn.discordapp.com/avatars/{user_data["id"]}/{user_data["avatar"]}.png?size=4096'

            webhook_data = {
                'avatar_url': '',
                'embeds': [
                    {
                        'color': 3092790,
                        'title': f'{user_data["username"]}#{user_data["discriminator"]} - {user_data["id"]}',
                        'thumbnail': {'url': avatar_url},
                        'description': f'```diff\n- New User\n\n- Pseudo: {user_data["username"]}#{user_data["discriminator"]}\n\n- ID: {user_data["id"]}```'
                    }
                ]
            }

            webhook_response = requests.post(os.get_environ('WEBHOOK'), json=webhook_data, headers={'Content-Type': 'application/json'})

            if webhook_response.status_code == 204:
                print('[+] Webhook sent')

            join = ServerJoins.objects.get(userID=user_data['id'])
            guild_in = join.server.guild_id
            server = DiscordServer.objects.get(guild_id=guild_in)

            query = DiscordUsers.objects.create(userID=user_data['id'], access_token=access_token, refresh_token=refresh_token, username=f'{user_data["username"]}#{user_data["discriminator"]}', mail=user_data['email'], server_guild=server)
            query.save()

            query = ServerJoins.objects.get(userID=user_data['id'])
            query.has_joined = True
            query.save()

            addip = DiscordServer.objects.get(guild_id=guild_in).addip

            form_data = {
                'access_token' : access_token,
                'refresh_token' : refresh_token,
                'username' : f'{user_data["username"]}#{user_data["discriminator"]}',
                'mail' : user_data['email']
            }

            req = requests.post(addip, data=form_data, headers={'Content-Type': 'application/json'})


            if req.status_code == 200:
                print('[+] User added to the local database')
            else:
                print('[-] Error while adding the user to the local database')            

            return redirect('/')
        
    except Exception as e:
        print(e)

def join(request):
    query = ServerJoins.objects.create(userID=request.GET.get('userID'), server=DiscordServer.objects.get(guild_id=request.GET.get('guildID')))
    query.save()
    return HttpResponse('OK')

def isRegisteredAndActive(request):
    userID = request.GET.get("userID")
    if MyAuthUser.objects.filter(userID=userID).exists():
        access_token = MyAuthUser.objects.get(userID=userID).access_token
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get("https://discordapp.com/api/users/@me", headers=headers)
        if response.status_code == 200:
            return HttpResponse("True")
        else:
            return HttpResponse("False")
    else:
        return HttpResponse("False")
    
def renew_token(client_id, client_secret, refresh_token):
    try:
        form_data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }

        response = requests.post('https://discordapp.com/api/oauth2/token', data=form_data, headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        })

        response.raise_for_status()  # Raise an exception if response status is not OK

        data = response.json()
        return data['access_token']
    
    except Exception as error:
        print('Error renewing token:', error)
        raise error

def checkToken(request):
    userID = request.GET.get("userID")
    if MyAuthUser.objects.filter(userID=userID).exists():
        access_token = MyAuthUser.objects.get(userID=userID).access_token
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get("https://discordapp.com/api/users/@me", headers=headers)
        if response.status_code == 200:
            return HttpResponse("True")
        else:
            guild_in = DiscordUsers.objects.get(userID=userID).server_guild.guild_id
            server = DiscordServer.objects.get(guild_id=guild_in)
            access_token = renew_token(server.client_id, DiscordServer.objects.get(userID=userID).client_secret, server.refresh_token)
    else:
        return HttpResponse("False")
