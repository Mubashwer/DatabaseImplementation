# The libraries we'll need
import sys, cgi, redirect, session, html

# Get the session and check if logged in
sess = session.Session(expires=60*20, cookie_path='/')
loggedIn = sess.data.get('loggedIn')
userType = sess.data.get('userType')

# send session cookie
print "%s\nContent-Type: text/html\n" % (sess.cookie)

# get form data
form = cgi.FieldStorage()

# ---------------------------------------------------------------------------------------------------------------------

print html.make_head("home.css", title="WWAG")

print html.make_navbar(loggedIn, userType)

print """
  
<body>
  <p>
    <div id="background">
      <p id="text"> WWAG </p>
      <p id="text2"> The Wil Wheaton Appreciation Guild </p>
  </div>
"""

print html.end_html

# Tidy up and free resources
sess.close()
