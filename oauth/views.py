from db.models import *
import os
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import datetime
from urllib.parse import quote_plus
from dotenv import load_dotenv
load_dotenv()
    
def verif(request, key):
    code = request.GET.get('code')

    valid = False

    if key == "test":
        redirect_url = "http://localhost:8000/verif/test/"
    else:
        redirect_url = os.getenv('OAUTH2_REDIRECT_URI')+key+"/"

    try:
        
        i = Bots.objects.get(name=key)
        form_data = {
                'client_id': i.client_id,
                'client_secret': i.client_secret,
                'grant_type': 'authorization_code',
                'redirect_uri': redirect_url,
                'scope': os.getenv('OAUTH2_SCOPES'),
                'code': code
            }

        token_response = requests.post('https://discordapp.com/api/oauth2/token', data=form_data, headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            })
        if token_response.status_code != 200:
            print('Token response status code:', token_response.status_code)
        else:
            valid = True


        token_data = token_response.json()
            
        if not valid:
            return HttpResponse('Error because of token response status code')

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
                        'title': f'New User',
                        'thumbnail': {'url': avatar_url},
                        'description': f'```diff\n- Username : {user_data["username"]}#{user_data["discriminator"]}\n\n- ID: {user_data["id"]}```'
                    }
                ]
        }

        join = UsersJoinServer.objects.filter(userID=user_data['id']).order_by('-id')[0]
        guild_in = join.server.guild_id

        webhook_response = requests.post(join.server.master.webhook_url, json=webhook_data, headers={'Content-Type': 'application/json'})
        if webhook_response.status_code == 204:
                print('[+] Webhook sent')
        else:
            print('[-] Webhook not sent')
            print(webhook_response.text)

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

        join.has_joined = True
        join.save()

        addip = join.server.master.addip
        role = DiscordServerJoined.objects.get(guild_id=guild_in).roleToGiveVerif
        try:
            req = requests.post(addip + "register_user/?id="+user_data["id"]+"&role="+role + "&server="+server.guild_id, headers={'Content-Type': 'application/x-www-form-urlencoded'})
            print("Communication with the bot went well")
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
    if DiscordUsers.objects.filter(userID=user_id,server_guild_id=guild_id).exists():
        for i in DiscordUsers.objects.filter(userID=user_id,server_guild_id=guild_id):
            i.delete()
        return JsonResponse("ok",status=200,safe=False)
    else:
        print(DiscordUsers.objects.filter(userID=user_id,server_guild_id=guild_id).exists())
        return HttpResponse("ko")
    

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
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def get_params(request):
    name = request.GET.get('name')
    req = Bots.objects.get(name=name)
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
    """
    if guild_id == 'all':
        master = request.GET.get('master')
        members = DiscordUsers.objects.filter(server_guild__master=Bots.objects.get(guild_id=master))
        return JsonResponse({
            'members': list(members.values())
        })
    else:
        if amount:
                master = Bots.objects.get(guild_id=guild_id)
                members = DiscordUsers.objects.filter(server_guild__master=master)[:int(amount)]
                return JsonResponse({
                    'members': list(members.values())
                })
        else:
            if DiscordServerJoined.objects.filter(guild_id=guild_id).exists():
                server = DiscordServerJoined.objects.get(guild_id=guild_id)
                master = server.master
                members = DiscordUsers.objects.filter(server_guild__master=master)
                return JsonResponse({
                    'members': list(members.values())
                })
            else:
                return JsonResponse({
                    'members': []
                })
            """
    master = Bots.objects.get(guild_id=guild_id)
    servs_linked = DiscordServerJoined.objects.filter(master=master)
    if DiscordUsers.objects.filter(server_guild__in=servs_linked).exists():
        members = DiscordUsers.objects.filter(server_guild__in=servs_linked)
        if int(amount) != 0:
            members = members[:int(amount)]
            return JsonResponse({
                'members': list(members[:int(amount)].values())
            })
        else:
            return JsonResponse({
                'members': list(members.values())
            })
    else:
        return JsonResponse({
            'members': []
        })

@csrf_exempt
def get_members_count(request):
    guild_id = request.GET.get('guild_id')
    members = DiscordUsers.objects.filter(server_guild=DiscordServerJoined.objects.get(guild_id=guild_id)).count()
    return JsonResponse({
        'count': members
    })

@csrf_exempt
def update_webhook(request):
    guild_id = request.GET.get('guild_id')
    webhook = request.GET.get('webhook')
    server = DiscordServerJoined.objects.get(guild_id=guild_id)
    master = server.master
    master.webhook_url = webhook
    master.save()
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
def set_button_content(request):
    guild_id = request.GET.get('guild_id')
    content = request.GET.get('content')
    Button.objects.filter(server=DiscordServerJoined.objects.get(guild_id=guild_id)).update(content=content)
    return HttpResponse('OK')

@csrf_exempt
def join(request):
    if UsersJoinServer.objects.filter(userID=request.GET.get('userID'), server=DiscordServerJoined.objects.get(guild_id=request.GET.get('guildID'))).exists():
        query = UsersJoinServer.objects.get(userID=request.GET.get('userID'), server=DiscordServerJoined.objects.get(guild_id=request.GET.get('guildID')))
        if query.has_joined:
            query.has_joined = False
            query.save()
    else:
        UsersJoinServer.objects.create(userID=request.GET.get('userID'), server=DiscordServerJoined.objects.get(guild_id=request.GET.get('guildID'))).save()
    return HttpResponse('OK')

@csrf_exempt
def left(request):
    if UsersJoinServer.objects.filter(userID=request.GET.get('userID'), server=DiscordServerJoined.objects.get(guild_id=request.GET.get('guildID'))).exists():
        query = UsersJoinServer.objects.get(userID=request.GET.get('userID'))
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

@csrf_exempt
def set_role(request):
    guild_id = request.GET.get('guild_id')
    role = request.GET.get('role')
    DiscordServerJoined.objects.filter(guild_id=guild_id).update(roleToGiveVerif=role)
    return HttpResponse('OK')

@csrf_exempt
def update_access_token(request):
    guild_id = request.GET.get('guild_id')
    user_id = request.GET.get('user_id')
    access_token = request.GET.get('access_token')
    refresh_token = request.GET.get('refresh_token')
    DiscordUsers.objects.filter(server_guild=DiscordServerJoined.objects.get(guild_id=guild_id), userID=user_id).update(access_token=access_token, refresh_token=refresh_token)
    return HttpResponse('OK')

@csrf_exempt
def get_subscription(request):
    guild_id = request.GET.get('guild_id')
    if Payment.objects.filter(buyer=Bots.objects.get(guild_id=guild_id)).exists():
        subscription_date = Payment.objects.get(buyer=Bots.objects.get(guild_id=guild_id)).date
        subscription_duration = Payment.objects.get(buyer=Bots.objects.get(guild_id=guild_id)).duration
        return JsonResponse({
            'subscription_date': subscription_date,
            'subscription_duration': subscription_duration
        })
    else:
        fake_date = datetime.datetime.now() - datetime.timedelta(days=1)
        fake_duration = 0
        return JsonResponse({
            'subscription_date': fake_date,
            'subscription_duration': fake_duration
        })

@csrf_exempt
def add_whitelist(request):
    guild_id = request.GET.get('guild_id')
    user_id = request.GET.get('user_id')
    author = request.GET.get('author')
    if Whitelist.objects.filter(server=Bots.objects.get(guild_id=guild_id), user_id=user_id).exists():
        Whitelist.objects.filter(server=Bots.objects.get(guild_id=guild_id), user_id=user_id, added_by = author).delete()
    Whitelist.objects.create(server=Bots.objects.get(guild_id=guild_id), user_id=user_id).save()
    return HttpResponse('OK')

@csrf_exempt
def rm_whitelist(request):
    guild_id = request.GET.get('guild_id')
    user_id = request.GET.get('user_id')
    Whitelist.objects.filter(server=Bots.objects.get(guild_id=guild_id), user_id=user_id).delete()
    return HttpResponse('OK')

@csrf_exempt
def get_whitelist(request):
    guild_id = request.GET.get('guild_id')
    try:
        whitelist = Whitelist.objects.filter(server=Bots.objects.get(guild_id=guild_id))
        return JsonResponse({
            'whitelist': list(whitelist.values())
        })
    except:
        return JsonResponse({
            'whitelist': []
        })