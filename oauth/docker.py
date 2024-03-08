import requests
from db.models import *
import os
from dotenv import load_dotenv
load_dotenv()

url = os.getenv('MASTER_DOCKER_URL')

def fetch_docker_master():
    url = "http://localhost:3000/health"
    response = requests.get(url)
    if not response.status_code == 200:
        print("Docker master is down")

    # updateList
    # bots = CurrentBots.objects.all()
    # body = { }
        
def add_bot(bot):
    urlAdd =  url+"add"
    botJson = {
        bot : 
        {
            "container_name" : bot.bot.name,
            "port" : bot.bot.addip.split(":")[1]
        }
    }
    print(botJson)
    response = requests.post(urlAdd, json=botJson)
    if not response.status_code == 200:
        print("Docker master is down")

def remove_bot(bot):
    urlRemove = url+"remove"
    botJson = {
        bot : 
        {
            "container_name" : bot.bot.name,
            "port" : bot.bot.addip.split(":")[1]
        }
    }
    response = requests.post(urlRemove, json=botJson)
    if not response.status_code == 200:
        print("Docker master is down")
