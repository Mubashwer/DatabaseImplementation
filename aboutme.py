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

print html.make_head("login.css", title="About Us")

print html.make_navbar(loggedIn, userType)

print """
  
<body>
    <div id="greeting">
    <h2> About Us </h2>
    <div id ="message">
            <p>The Wil Wheaton Appreciation Guild (WWAG)* is a company which creates videos of exciting gameplay, including such games as Minecraft and FIFA 15. These videos are uploaded to another website for your enjoyment.</p>
            <p>Since beginning in 2001, WWAG has become one of the most successful group of players in the Asia-Pacific region. Players from many countries participate in the different gameplays, and have helped WWAG in completing it's world-firsts and other achievements. On Friday nights, a new instance run will be uploaded of the players completing stand alone game sessions. These include finishing in-game achievements, or trying to complete a game's content in as short a time as possible. The games are played on one of the gaming platforms available to WWAG.</p>
            <p>Please note that whilst most of the videos are for free, there are some that are only available to premium members, and people who have donated to the crowdfunding initiatives.</p>
            <pre />
            <pre />
            <p>*No association to the celebrity, Wil Wheaton</p>
    </div>
    </div>
"""

print html.end_html

# Tidy up and free resources
sess.close()
