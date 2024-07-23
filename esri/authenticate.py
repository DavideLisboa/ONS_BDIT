import requests
import json


def authenticate(portal_url, username, password):
    login_url = f"{portal_url}/portal/sharing/rest/generateToken"
    params = {
        "username": username,
        "password": password,
        "referer": portal_url,
        "f": "json",
    }
    response = requests.post(login_url, data=params)
    token = json.loads(response.text)["token"]
    return token
