import requests
import json
from urllib import request
from arcgis.gis import GIS
from esri.remove_item import remove_item


def download_file(portal_url, username, password, excel_path, token):
    gis = GIS(portal_url + '//portal', username, password)

    query_url = f"{portal_url}/server/rest/services/Hosted/Eletrobras_ONS/FeatureServer/2/query"
    params = {
        "where": f"status = 'novo'",
        "f": "json",
        "token": token,
        "outFields": "objectid,nome_equipamento,status,id",
    }
    response = requests.get(query_url, params=params)
    data = json.loads(response.text)

    if "features" in data and len(data["features"]) > 0:
        objectid = data["features"][0]["attributes"]["objectid"]
        id = data["features"][0]["attributes"]["id"]
        name = data["features"][0]["attributes"]["nome_equipamento"]
        data_url = "{}/portal/sharing/content/items/{}/data".format(
            portal_url, id)

        req = request.urlopen(data_url + "?token=" + token)
        CHUNK = 16 * 1024
        filename = f'{excel_path}\{name}'
        with open(filename, 'wb') as fp:
            while True:
                chunk = req.read(CHUNK)
                if not chunk:
                    break
                fp.write(chunk)
        remove_item(portal_url, id, token)
        return objectid
