# The libraries we'll need
import sys, cgi, redirect, session, MySQLdb

# Get the session and check if logged in
sess = session.Session(expires=60*20, cookie_path='/')
#loggedIn = sess.data.get('loggedIn') #anybody can access this page
form = cgi.FieldStorage()

# ---------------------------------------------------------------------------------------------------------------------
# send session cookie
print "%s\nContent-Type: text/html\n" % (sess.cookie)

print """
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta name="keywords" content="" />
<meta name="description" content="" />
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<title>About Us</title>
<link href="css/About.css" rel="stylesheet" type="text/css" media="screen" />
</head>
<body>
"""
print """
<div id="header">
            <div id="navbar">
                <ul>
            <li><a href="do_logout.py" style="text-decoration:none;color:#fff">Log Out</a></li>
            <li><a href="aboutme.py" style="text-decoration:none;color:#fff">About Us</a></li>
            <li><a href="players.py" style="text-decoration:none;color:#fff">Players</a></li>
            <li><a href="games.py" style="text-decoration:none;color:#fff">Games</a></li>
            <li><a href="instance_runs.py" style="text-decoration:none;color:#fff">Instance Runs</a></li>
            <li><a href="achievements.py" style="text-decoration:none;color:#fff">Achievements</a></li>
            <li><a href="viewers.py" style="text-decoration:none;color:#fff">Viewers</a></li>
            <li><a href="videos_modify.py" style="text-decoration:none;color:#fff">Videos</a></li>
            <li><a href="home.py" style="text-decoration:none;color:#fff">Home</a></li>
                </ul>
            </div>
            
  </div>
""" 
print """
<h1 id="title">About WWAG</h1>
"""
print """            
    <body>
        <div id="background">
            <p>The Wil Wheaton Appreciation Guild (WWAG)* is a company which creates videos of exciting gameplay, including such games as Minecraft and FIFA 15. These videos are uploaded to another website for your enjoyment.</p>
            <p>Since beginning in 2001, WWAG has become one of the most successful group of players in the Asia-Pacific region. Players from many countries participate in the different gameplays, and have helped WWAG in completing it's world-firsts and other achievements. On Friday nights, a new instance run will be uploaded of the players completing stand alone game sessions. These include finishing in-game achievements, or trying to complete a game's content in as short a time as possible. The                     games are played on one of the gaming platforms available to WWAG.</p>
            <p>Please note that whilst most of the videos are for free, there are some that are only available to premium members, and people who have donated to the crowdfunding initiatives.</p>
            <pre />
            <pre />
            <p>*No association to the celebrity, Wil Wheaton</p>
"""
print """
    </body>
    </html>
"""
