from flask import Flask, request, render_template
import processor
from calculations import Closest_boxes
from dbi import select_voter_links, create_connection
from api import poll_locs, parse_polls
import sys


def full_dict(address, key):
    state = processor.state(address)
    conn = create_connection("fulldata.sqlite")

    # Getting voter registration links from the database. This returns [state, registration, onlinereg(optional), registration_check(optional)]
    voter_links = select_voter_links(conn, state)[0]
    if voter_links[2] == "404" and voter_links[3] == "404":
        links = {"Register to Vote": voter_links[1]}
    elif voter_links[2] == "404":
        links = {"Register to Vote": voter_links[1], "Register online for your mail-in ballot": voter_links[3]}
    elif voter_links[3] == "404":
        links = {"Register to Vote  ": voter_links[1], "Register online for your mail-in ballot": voter_links[2]}
    else:
        links = {"Register to Vote": voter_links[1], "Register online for your mail-in ballot": voter_links[2], "Check your registration": voter_links[3]}

    # This returns a json/dict.
    poll_locations = poll_locs(address, key)

    # The parsed version of the poll json. The return object is formatted as
    # {"polling_stations": {address: {"name": name, "time": {day: time}}}, "early_voting": {address1: {"name": name, "time": {day1: hours, day2: hours...}}, {address2: {same}...}}}}
    processed = parse_polls(poll_locations)

    # This returns a dict of {address1: (lat, lng) ... addressN: (lat, lng)}
    mailboxes = Closest_boxes(address=address, key=key).create_address()

    return {"voter_links": links, "polling_locations": processed, "boxes": mailboxes}


app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('vip.html')

@app.route('/', methods=['POST'])
def my_form_post(key=sys.argv[1]):
    if len(sys.argv) == 1:
        raise KeyError("Too few arguments supplied")
    if len(sys.argv) > 2:
        raise KeyError("Too many arguments supplied")

    text = request.form['text']
    ppx = processor.address_checker(text)
    if ppx[1] == 0:
        return render_template('info.html', text=full_dict(ppx[0], key))
    else:
        return ppx

if __name__ == '__main__':
    app.run()
