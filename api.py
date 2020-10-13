import requests
import json
import re

def poll_locs(address, key):
    base_url = "https://www.googleapis.com/civicinfo/v2/voterinfo"
    url = "{}?address={}&key={}".format(base_url, address, key)
    request = requests.get(url=url)
    return request.json()


def parse_address(station_info):
    addr = station_info["line1"]
    city = station_info["city"]
    state = station_info["state"]
    zip = station_info["zip"]

    try:
        addr2 = station_info["line2"]
        address = "{}, {}, {}, {}, {}".format(addr, addr2, city, state, zip)
    except KeyError:
        address = "{}, {}, {}, {}".format(addr, city, state, zip)

    return address


def parse_hours(hours_info):
    hours = hours_info.split("\n")
    if len(hours) == 1:
        spt = hours[0].split(": ")
        return {spt[0]: spt[1]}
    else:
        hours = hours[:7]
        ret = {}
        for time in hours:
            day = time[:3]
            time = re.findall(r"\d\d: (.*)", time)

            try:
                ret[day] = time[0]
            except IndexError:
                pass

        return ret


def parse_polls(info):

    ps = {}
    ev = {}

    try:
        poll_stations = info["pollingLocations"]
        for station in poll_stations:
            st = station["address"]
            address = parse_address(st)
            name = st["locationName"]

            time = parse_hours(station["pollingHours"])

            ps[address] = {"name": name, "time": time}
    except KeyError:
        pass
    try:
        early_voting = info["earlyVoteSites"]

        for station in early_voting:
            st = station["address"]
            address = parse_address(st)
            name = st["locationName"]

            time = parse_hours(station["pollingHours"])

            ev[address] = {"name": name, "time": time}
    except KeyError:
        pass

    return {"polling_stations": ps, "early_voting": ev}


def geoencoding(address, key):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    url = "{}?address={}&key={}".format(base_url, address, key)
    request = requests.get(url=url)
    return request.json()

