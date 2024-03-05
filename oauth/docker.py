import requests

def fetch_docker_master():
    url = "http://localhost:3000/docker/master"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None