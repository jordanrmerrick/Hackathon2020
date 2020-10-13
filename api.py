import requests
import json

def poll_locs(address, key):
    base_url = "https://www.googleapis.com/civicinfo/v2/voterinfo"
    url = "{}?address={}&key={}".format(base_url, address, key)
    request = requests.get(url=url)
    return request.json()


def geoencoding(address, key):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    url = "{}?address={}&key={}".format(base_url, address, key)
    request = requests.get(url=url)
    return request.json()

