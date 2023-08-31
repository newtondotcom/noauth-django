from db.models import *
import os
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from urllib.parse import quote_plus
from dotenv import load_dotenv
load_dotenv()

def callback(request):
    code = request.GET.get('code')

    form_data = {
        'client_id': os.getenv('OAUTH2_CLIENT_ID'),
        'client_secret': os.getenv('OAUTH2_CLIENT_SECRET'),
        'grant_type': 'authorization_code',
        'redirect_uri': os.getenv('OAUTH2_REDIRECT_URI'),
        'scope': os.getenv('OAUTH2_CLIENT_ID'),
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

        print(f'[+] {user_data["username"]}#{user_data["discriminator"]}')
        avatar_url = f'https://cdn.discordapp.com/avatars/{user_data["id"]}/{user_data["avatar"]}.png?size=4096'

        webhook_data = {
                'embeds': [
                    {
                        'color': 3092790,
                        'title': f'{user_data["username"]}#{user_data["discriminator"]} - {user_data["id"]}',
                        'thumbnail': {'url': avatar_url},
                        'description': f'```diff\n- New User\n\n- Username : {user_data["username"]}#{user_data["discriminator"]}\n\n- ID: {user_data["id"]}```'
                    }
                ]
        }

        join = ServerJoins.objects.get(userID=user_data['id'])
        guild_in = join.server.guild_id

        master = Bots.objects.get(guild_id=guild_in)
    
        webhook_response = requests.post(master.webhook_url, json=webhook_data, headers={'Content-Type': 'application/json'})
        if webhook_response.status_code == 204:
                print('[+] Webhook sent')

        server = DiscordServerJoined.objects.get(guild_id=guild_in)

        exists = DiscordUsers.objects.filter(server_guild=server,userID=user_data['id']).exists()
        if exists:
            query = DiscordUsers.objects.get(server_guild=server,userID=user_data['id'])
            query.access_token = access_token
            query.refresh_token = refresh_token
            query.username = f'{user_data["username"]}#{user_data["discriminator"]}'
            query.email = user_data['email']
            query.save()
        else:
            query = DiscordUsers.objects.create(userID=user_data['id'], access_token=access_token, refresh_token=refresh_token, username=f'{user_data["username"]}#{user_data["discriminator"]}', email=user_data['email'], server_guild=server)
            query.save()

        query = ServerJoins.objects.get(userID=user_data['id'])
        query.has_joined = True
        query.save()

        addip = master.addip

        try:
            req = requests.post(addip + "register_user/?id="+user_data["id"], headers={'Content-Type': 'application/x-www-form-urlencoded'})
            print(req.text)
        except requests.exceptions.RequestException as e:
            print("Error:", e)

        return redirect(index)
        
    except Exception as e:
        print(e)
        return HttpResponse('Error')

@csrf_exempt
def dl_user(request):
    user_id = request.GET.get("user_id")
    guild_id = request.GET.get("guild_id")
    if DiscordUsers.objects.filter(userID=user_id,guild=DiscordServerJoined.objects.get(guild_id=guild_id)).exists():
        DiscordUsers.objects.filter(userID=user_id,guild=DiscordServerJoined.objects.get(guild_id=guild_id)).delete()
        return HttpResponse("ok")
    else:
        return HttpResponse("ko")

@csrf_exempt
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
    
@csrf_exempt
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
            server = DiscordServerJoined.objects.get(guild_id=guild_in)
            access_token = renew_token(server.client_id, DiscordServerJoined.objects.get(userID=userID).client_secret, server.refresh_token)
    else:
        return HttpResponse("False")

@csrf_exempt
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def get_params(request):
    name = request.GET.get('name')
    req = DiscordServerJoined.objects.get(name=name)
    return JsonResponse({
        'clientId': req.client_id,
        'clientSecret': req.client_secret,
        'token': req.token,
        'guildId': req.guild_id,
        'owner': req.owner_discord_id,
        'webhook': req.webhook_url,
        'color': req.color
    })

@csrf_exempt
def get_ip_master(request):
    guild_id = request.GET.get('guild_id')
    req = Bots.objects.get(guild_id=guild_id)
    return JsonResponse({
        'ip': req.addip
    })

@csrf_exempt
def get_members(request):
    guild_id = request.GET.get('guild_id')
    amount = request.GET.get('amount')
    if amount:
        members = DiscordUsers.objects.filter(server_guild=DiscordServerJoined.objects.get(guild_id=guild_id))[:int(amount)]
    else:
        members = DiscordUsers.objects.filter(server_guild=DiscordServerJoined.objects.get(guild_id=guild_id))
    return JsonResponse({
        'members': list(members.values())
    })

@csrf_exempt
def update_webhook(request):
    guild_id = request.GET.get('guild_id')
    webhook = request.GET.get('webhook')
    DiscordServerJoined.objects.filter(guild_id=guild_id).update(webhook_url=webhook)
    return HttpResponse('OK')

@csrf_exempt
def get_button(request):
    guild_id = request.GET.get('guild_id')
    buttons = Button.objects.filter(server=DiscordServerJoined.objects.get(guild_id=guild_id))
    buttons.values()[0]
    return JsonResponse({
        'button': list(buttons.values())
    })

@csrf_exempt
def set_button_graphic(request):
    guild_id = request.GET.get('guild_id')
    image = quote_plus(request.GET.get('image'))
    color = request.GET.get('color')
    Button.objects.filter(server=DiscordServerJoined.objects.get(guild_id=guild_id)).update(image=image, color=color)
    return HttpResponse('OK')

@csrf_exempt
def set_button_text(request):
    guild_id = request.GET.get('guild_id')
    name = request.GET.get('name')
    title = request.GET.get('title')
    description = request.GET.get('description')
    footer = request.GET.get('footer')
    Button.objects.filter(server=DiscordServerJoined.objects.get(guild_id=guild_id)).update(name=name, title=title, description=description, footer=footer)
    return HttpResponse('OK')

@csrf_exempt
def join(request):
    if ServerJoins.objects.filter(userID=request.GET.get('userID'), server=DiscordServerJoined.objects.get(guild_id=request.GET.get('guildID'))).exists():
        query = ServerJoins.objects.get(userID=request.GET.get('userID'), server=DiscordServerJoined.objects.get(guild_id=request.GET.get('guildID')))
        if query.has_joined:
            query.has_joined = False
            query.save()
        return HttpResponse('OK')
    else:
        ServerJoins.objects.create(userID=request.GET.get('userID'), server=DiscordServerJoined.objects.get(guild_id=request.GET.get('guildID'))).save()
        return HttpResponse('OK')

@csrf_exempt
def left(request):
    if ServerJoins.objects.filter(userID=request.GET.get('userID'), server=DiscordServerJoined.objects.get(guild_id=request.GET.get('guildID'))).exists():
        query = ServerJoins.objects.get(userID=request.GET.get('userID'))
        if query.has_joined:
            query.has_joined = False
            query.save()
        return HttpResponse('OK') 
    return HttpResponse('OK')
    
@csrf_exempt
def guild_joined(request):
    guild_id = request.GET.get('guild_id')
    guild_joined = request.GET.get('guild_joined')
    DiscordServerJoined.objects.create(master=Bots.objects.get(guild_id=guild_id), guild_id=guild_joined)
    return HttpResponse('OK')

@csrf_exempt
def guild_left(request):
    guild_id = request.GET.get('guild_id')
    guild_left = request.GET.get('guild_left')
    DiscordServerJoined.objects.filter(master=Bots.objects.get(guild_id=guild_id), guild_id=guild_left).delete()
    return HttpResponse('OK')
