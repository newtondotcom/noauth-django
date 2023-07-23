from db.models import *
import os
from requests_oauthlib import OAuth2Session
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import requests
from django.core import serializers
import json
from dotenv import load_dotenv
load_dotenv()

OAUTH2_CLIENT_ID = os.environ['OAUTH2_CLIENT_ID']
OAUTH2_CLIENT_SECRET = os.environ['OAUTH2_CLIENT_SECRET']
OAUTH2_REDIRECT_URI = 'http://localhost:8000/callback'

API_BASE_URL = os.environ.get('API_BASE_URL', 'https://discordapp.com/api')
AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'
TOKEN_URL = API_BASE_URL + '/oauth2/token'

if 'http://' in OAUTH2_REDIRECT_URI:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

def token_updater(token,request):
    request.session['oauth2_token'] = token


def make_session(token=None, state=None, scope=None):
    return OAuth2Session(
        client_id=OAUTH2_CLIENT_ID,
        token=token,
        state=state,
        scope=scope,
        redirect_uri=OAUTH2_REDIRECT_URI,
        auto_refresh_kwargs={
            'client_id': OAUTH2_CLIENT_ID,
            'client_secret': OAUTH2_CLIENT_SECRET,
        },
        auto_refresh_url=TOKEN_URL,
        token_updater=token_updater)

def index(request):
    scope = request.args.get(
        'scope',
        'identify email connections guilds guilds.join')
    discord = make_session(scope=scope.split(' '))
    authorization_url, state = discord.authorization_url(AUTHORIZATION_BASE_URL)
    request.session['oauth2_state'] = state
    return redirect(authorization_url)

def callback(request):
    authorization_code = request.GET['code']
    token_request_data = {
        'code': authorization_code,
        'redirect_uri': OAUTH2_REDIRECT_URI,
        'grant_type': 'authorization_code'
    }

    # Make a POST request to Discord's token URL to exchange the authorization code for an access token
    response = requests.post("https://discord.com/api/oauth2/token", data=token_request_data, auth=(OAUTH2_CLIENT_ID, OAUTH2_CLIENT_SECRET))

    # Parse the response JSON to extract the access token
    token_data = response.json()
    print(token_data)
    access_token = token_data.get('access_token')
    refresh_token = token_data.get('refresh_token')
    request.session['oauth2_token'] = access_token
    request.session['oauth2_refresh'] = refresh_token
    return redirect('/me')

def fetch_discord_data(endpoint, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(endpoint, headers=headers)
    return response.json()

def me(request):
    access_token = request.session.get('oauth2_token')
    refresh_token = request.session.get('oauth2_refresh')

    if not access_token:
        return JsonResponse({"error": "Access token not found in session. Please authorize the application first."})

    user = fetch_discord_data(API_BASE_URL + '/users/@me', access_token)
    guilds = fetch_discord_data(API_BASE_URL + '/users/@me/guilds', access_token)

    guilds = json.loads(guilds)
    servers = []
    for guild in guilds:



    if not DiscordUsers.objects.filter(userID=user['id']).exists():
        query = DiscordUsers.objects.create(userID=user['id'], access_token=access_token, username=user['username'], refresh_token=refresh_token)
        query.save()
    else:
        query = DiscordUsers.objects.get(userID=user['id'])
        query.access_token = access_token
        query.save()

    return JsonResponse({"user": user, "guilds": guilds})


def countuser(request):
    countuser = DiscordUsers.objects.all().count()
    return JsonResponse({"countuser": countuser})

def get_x_users(request,x):
    users = DiscordUsers.objects.all()[:x]
    user_date = serializers.serialize('json', users)
    return JsonResponse({"users": user_date})