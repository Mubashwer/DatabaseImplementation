import sys, cgi, redirect, session, MySQLdb
from common import *
from html import *

# Get the session and check if logged in
sess = session.Session(expires=60*20, cookie_path='/')
loggedIn = sess.data.get('loggedIn')
userType = sess.data.get('userType')

# send session cookie
print "%s\nContent-Type: text/html\n" % (sess.cookie)

# get form data
form = cgi.FieldStorage()

venue_id = form.getvalue('venue_id')
title = 'WWAG Venue'
if venue_id == None:
    title += 's'
    venue_id = ''
    
print make_head('video_modify.css',title=title)
print make_navbar(loggedIn, userType)

db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003g29", "enigma29", "info20003g29", 3306)
c = db.cursor()

query = "SELECT * FROM Venue WHERE VenueId LIKE %s"

c.execute(query, ('%' + str(venue_id) + '%',))

rows = results_as_dicts(c)
                         
print "<table class='gridtable' align='center'>"
print "<tr><th>VenueID</th><th>VenueName</th>"
if venue_id != '':
    print "<th>VenueDescription</th>"
print "</tr>"

for row in rows:
    row_html = ''
    row_html += wrap_td(str(row['VenueID']))
    row_html += wrap_td("<a href='venues.py?venue_id={}'>".format(row["VenueID"]) + row['VenueName'] + "</a>")
    if venue_id != '':
        row_html += wrap_td(str(row['VenueDescription']))
    row = wrap_tr(row_html)
    print row
print "</table>"
print end_html
