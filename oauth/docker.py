import requests

def fetch_docker_master():
    url = "http://localhost:8000"
    response = requests.get(url)
    if response.status_code == 200:
        return "Success"
    else:
        return None