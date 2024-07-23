import requests
import json


def update_status(portal_url, id_to_update, new_status, error, token):
    update_url = f"{portal_url}/server/rest/services/Hosted/Eletrobras_ONS/FeatureServer/2/updateFeatures"
    if error:
        params = {
            "features": json.dumps([{
                "attributes": {
                    "objectid": id_to_update,
                    "status": new_status,
                    "mensagem": error,
                }
            }]),
            "token": token,
            "f": "json",
        }
    else:
        params = {
            "features": json.dumps([{
                "attributes": {
                    "objectid": id_to_update,
                    "status": new_status
                }
            }]),
            "token": token,
            "f": "json",
        }
        response = requests.post(update_url, data=params)
        result = json.loads(response.text)
        if "updateResults" in result and result["updateResults"][0]["success"]:
            print(f"Status updated to '{new_status}' for ID {id_to_update}")
        else:
            print(f"Failed to update status for ID {id_to_update}")
