from flask import Flask, request, render_template, abort, url_for
import processor
from calculations import Closest_boxes

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('vip.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    ppx = processor.address_checker(text)
    if ppx[1] == 0:
        t = Closest_boxes(address=ppx[0], key="AIzaSyCpU_v3EsEQKgAWQXmRBAF_6rr36wFFgMY").create_address()
        return str(t)
    else:
        return ppx

@app.route('/info')
def info():
    return render_template('info.html')

if __name__ == '__main__':
    app.run()

"""
Idea

Creating a flask-based website that allows people to check if they're registered to vote,
and where their closest polling place(s) are. It will also show you where your closest USPS mailbox is.

Pulls info from an SQLite database!

"""