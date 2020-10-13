from math import radians, cos, sqrt
from dbi import select_from_zip, select_from_id, create_connection
from api import *
import usaddress


def distance(lat1, lon1, lat2, lon2):
    x = radians(lon1 - lon2) * cos(radians((lat1 + lat2) / 2))
    y = radians(lat1 - lat2)
    # 6371000 is the radius of earth, used to triangulate distance!
    dist = 6371000 * sqrt((x * x) + (y * y))

    return dist

class Closest_boxes(object):

    def __init__(self, address, key):
        self.address = address
        self.key = key

    def geoencode(self):
        geo = geoencoding(self.address, self.key)
        g = geo["results"][0]["geometry"]
        location = g["location"]
        lat1 = location["lat"]
        lon1 = location["lng"]

        return [lat1, lon1]

    def parse_address(self):
        try:
            ret = usaddress.tag(self.address)
        except usaddress.RepeatedLabelError:
            ret = "Please enter a valid address."

        return ret

    def mailbox_loc(self):
        conn = create_connection("fulldata.sqlite")
        parsed = self.parse_address()[0]
        zipcode = parsed["ZipCode"]

        return select_from_zip(conn, zipcode)

    def closest_boxes(self):
        high, med, low = -1, -1, -1
        hi, mi, li = 0, 0, 0

        selfaddr = self.geoencode()
        boxes = self.mailbox_loc()
        for box in boxes:
            lat = box[-2]
            lon = box[-1]
            dist = distance(float(lat), float(lon), float(selfaddr[0]), float(selfaddr[1]))
            if high == -1 or med == -1 or low == -1:
                high, med, low = dist, dist, dist
            elif dist <= low:
                high, med, low, hi, mi, li = med, low, dist, mi, li, box[0]
            elif low < dist <= med:
                high, med, hi, mi = med, dist, mi, box[0]
            elif dist > med <= high:
                high, hi = dist, box[0]
            else:
                pass

        conn = create_connection("fulldata.sqlite")
        r0 = select_from_id(conn, hi)
        r1 = select_from_id(conn, mi)
        r2 = select_from_id(conn, li)
        ret = [r0, r1, r2]
        return ret

    def create_address(self):
        box_locs = self.closest_boxes()
        box_locs.reverse()
        ret = {}
        for box in box_locs:
            box_ = box[0]
            addr = box_[1]
            city = box_[2]
            state = box_[3]
            zipcode = box_[4]
            full = "{}, {}, {}, {}".format(addr, city, state, zipcode)
            ret[full] = (box_[-2], box_[-1])

        return ret
