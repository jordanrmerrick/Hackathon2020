# MLH Fellowship Hackathon - Voting Information Project

### For the first-week hackathon project, I wanted to build a webapp that will allow people to find as much useful information on how and where to vote as possible. My gripe with most services that are already doing this is that they only have *some* information and I end up having to go to 2-3 websites to find everything. I'm trying to correct this!

## The Technicals
This webapp is built on [flask](https://flask.palletsprojects.com/en/1.1.x/), a lightweight framework for Python.
It also makes heavy use of an sqlite3 database, something that's included in the github repo! (Warning, it's >32MB and has over somewhere around 200,000 rows.)

The website takes very little user input, just a valid address.
From there it will give a bunch of useful info, including registration info for your state, your polling place, where you can vote early, and where the 3 closest USPS boxes are to mail-in your ballot.
It does this through rendered templates, an awesome feature in flask which allows you to change your webpage dynamically.

## To-Do
 [ ] Build the actual webpage

 [ ] Implement a static map from [Google's Map API](https://developers.google.com/maps/documentation/maps-static/overview) so that you can see mailboxes near you
 
 [ ] Put in the CSS to make it look nice, change the font, add nice colors, etc
 
 [ ] Add some JS to make it look even nicer? I can do this with OCaml and compile it to JS bytecode since I don't know any JS
