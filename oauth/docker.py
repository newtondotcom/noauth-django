import requests
from db.models import *

def fetch_docker_master():
    url = "http://localhost:3000/health"
    response = requests.get(url)
    if not response.status_code == 200:
        print("Docker master is down")

    # updateList
    # bots = CurrentBots.objects.all()
    # body = { }
