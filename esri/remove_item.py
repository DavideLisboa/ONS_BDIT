import requests
import json


def remove_item(portal_url, id_to_remove, token):
    delete_url = f"{portal_url}/portal/sharing/rest/content/users/portaladmin/deleteItems"
    params = {
        "f": "json",
        "token": token,
        "items": id_to_remove
    }
    response = requests.post(delete_url, data=params)
    result = json.loads(response.text)
