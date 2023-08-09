from db.models import *
import os
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import requests
import json
from dotenv import load_dotenv
load_dotenv()


def register(request):
    access_token = request.GET.get("access_token")
    refresh_token = request.GET.get("refresh_token")
    username = request.GET.get("username")
    userID = request.GET.get("userID")
    if DiscordUsers.objects.filter(userID=userID).exists():
        user = DiscordUsers.objects.get(userID=userID)
        user.access_token = access_token
        user.refresh_token = refresh_token
        user.username = username
        user.save()
    else:
        query = DiscordUsers.objects.create(userID=userID, access_token=access_token, refresh_token=refresh_token, username=username)
        query.save()
    return HttpResponse("OK")

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
    
def addServerMember(request):
    userID = request.GET.get("userID")
    query = MyServerMembers.objects.create(userID=userID)
    query.save()

def removeServerMember(request):
    userID = request.GET.get("userID")
    MyServerMembers.objects.filter(userID=userID).delete()


import boto3

session = boto3.Session(
    aws_access_key_id='AWS_ACCESS_KEY_ID',
    aws_secret_access_key='AWS_SECRET_ACCESS_KEY',
)
s3 = session.resource('s3')
# Filename - File to upload
# Bucket - Bucket to upload to (the top level directory under AWS S3)
# Key - S3 object name (can contain subdirectories). If not specified then file_name is used
s3.meta.client.upload_file(Filename='input_file_path', Bucket='bucket_name', Key='s3_output_key')