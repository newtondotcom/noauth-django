from db.models import *
from db.signals import add_removed_user
from oauth.subscriptions import *
import os
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q, F
import requests
import datetime
from urllib.parse import quote_plus
from dotenv import load_dotenv
from oauth.token import *
load_dotenv()
    
@csrf_exempt    
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

        # the webhook is now sent by the bot
        #webhook_response = requests.post(join.server.master.webhook_url, json=webhook_data, headers={'Content-Type': 'application/json'})
        #if webhook_response.status_code == 204:
                #print('[+] Webhook sent')
        #else:
            #print('[-] Webhook not sent')
            #print(webhook_response.text)

        exists = NoAuthUsers.objects.filter(userID=user_data['id'], master=i).exists()
        if exists:
            query = NoAuthUsers.objects.get(userID=user_data['id'], master=i)
            query.access_token = access_token
            query.refresh_token = refresh_token
            query.save()
        else:
            NoAuthUsers.objects.create(userID=user_data['id'], access_token=access_token, refresh_token=refresh_token, username=user_data['username'], email=user_data['email'], master=i).save()

        join.has_joined = True
        join.save()

        addip = i.addip
        role = DiscordServerJoined.objects.get(guild_id=guild_in).roleToGiveVerif
        count  = NoAuthUsers.objects.filter(master=i).count()
        webhook = i.webhook_url
        try:
            req = requests.post(addip + "register_user/?id="+user_data["id"]+"&role="+role + "&server="+guild_in+"&count="+str(count)+"&webhook="+webhook)
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
    master = Bots.objects.get(guild_id=guild_id)
    if NoAuthUsers.objects.filter(userID=user_id, master=master).exists():
        NoAuthUsers.objects.filter(userID=user_id, master=master).delete()
        add_removed_user(master)
        return JsonResponse("ok",status=200,safe=False)
    else:
        return JsonResponse("ok",status=200,safe=False)
    

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
    master = Bots.objects.get(guild_id=guild_id)
    members = NoAuthUsers.objects.filter(master=master)
    if members.exists():
        return JsonResponse({
            'members': list(members.values()),
            'speed': master.speed
        })
    else:
        return JsonResponse({
            'members': []
        })

@csrf_exempt
def get_members_per_server(request):
    guild_id = request.GET.get('guild_id')
    server = DiscordServerJoined.objects.get(guild_id=guild_id)
    members_of_server = UsersJoinServer.objects.filter(server=server)
    master = server.master
    members_verified = NoAuthUsers.objects.filter(master=master, userID__in=members_of_server.values('userID'))
    if members_verified.exists():
        return JsonResponse({
            'members': list(members_verified.values())
        })
    else:
        return JsonResponse({
            'members': []
        })

@csrf_exempt
def get_members_count(request):
    guild_id = request.GET.get('guild_id')
    server = DiscordServerJoined.objects.get(guild_id=guild_id)
    members_of_server = UsersJoinServer.objects.filter(server=server)
    master = server.master
    members_verified = NoAuthUsers.objects.filter(master=master)
    members_count = members_of_server.annotate(
        verified_members_count=Count('user__id', filter=Q(user__in=members_verified))
    ).values('verified_members_count')

    return JsonResponse({
        'count': members_count
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
    NoAuthUsers.objects.filter(userID=user_id, master=Bots.objects.get(guild_id=guild_id)).update(access_token=access_token, refresh_token=refresh_token)
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
    
@csrf_exempt
def test_users(request,bot):
    master = Bots.objects.get(name=bot)
    users = NoAuthUsers.objects.filter(master=master)
    for i in users:
        test_token(master.guild_id, i.userID, i.access_token, i.refresh_token, {'clientId': master.client_id, 'clientSecret': master.client_secret})
    users = NoAuthUsers.objects.filter(master=master)
    return JsonResponse({
        'users': list(users.values())
    })

@csrf_exempt
def check_subscription(request):
    check_payments()
    return HttpResponse('OK')

@csrf_exempt
def get_revoked(request):
    guild_id = request.GET.get('guild_id')
    master = Bots.objects.get(guild_id=guild_id)
    revoked = Counters.objects.filter(master=master,name="userDeleted").get().count
    return JsonResponse({
        'revoked': revoked
    })

@csrf_exempt
def set_speed(request):
    guild_id = request.GET.get('guild_id')
    speed = request.GET.get('speed')
    master = Bots.objects.get(guild_id=guild_id)
    master.speed = speed
    master.save()
    return HttpResponse('OK')

@csrf_exempt
def get_whitelist_rules(request):
    guild_id = request.GET.get('guild_id')
    master = Bots.objects.get(guild_id=guild_id)
    whitelist = Whitelist.objects.filter(server=master)
    rules = WlRules.objects.filter(whitelist__in=whitelist)
    annotations = rules.annotate(
        user_id=F('whitelist__user_id')
    )
    return JsonResponse({
        'rules': list(annotations.values())
    })

@csrf_exempt
def rm_whitelist_rule(request):
    rule_id = request.GET.get('rule_id')
    if WlRules.objects.filter(id=rule_id).exists():
        WlRules.objects.filter(id=rule_id).delete()
        print('Rule deleted')
        return HttpResponse('OK')
    else:
        print('Rule not found')
        return HttpResponse('Rule not found')

@csrf_exempt
def add_whitelist_rule(request):
    guild_id = request.GET.get('guild_id')
    user_id = request.GET.get('user_id')
    joinlimit = request.GET.get('joinlimit')
    sessionlimit = request.GET.get('sessionlimit')
    if not Whitelist.objects.filter(server=Bots.objects.get(guild_id=guild_id), user_id=user_id).exists():
        Whitelist.objects.create(server=Bots.objects.get(guild_id=guild_id), user_id=user_id).save()
    user = Whitelist.objects.get(server=Bots.objects.get(guild_id=guild_id), user_id=user_id)
    WlRules.objects.create(whitelist=user, joinlimit=joinlimit, sessionlimit=sessionlimit).save()
    return HttpResponse('OK')
