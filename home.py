# The libraries we'll need
import sys, cgi, redirect, session, MySQLdb, warnings

# Get a DB connection
db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003", "cisds", "info20003", 3306)
cursor = db.cursor()

# What came on the URL string?
params = cgi.FieldStorage()

foundParam=0

# Check if the parameter we are looking for was passed
if params.has_key('paramName'):

    foundParam=1


warnings.filterwarnings('error', category=MySQLdb.Warning)
# Get the session and check if logged in
sess = session.Session(expires=60*20, cookie_path='/')
loggedIn = sess.data.get('loggedIn')
userType = sess.data.get('userType')

# send session cookie
print "%s\nContent-Type: text/html\n" % (sess.cookie)

# get form data
form = cgi.FieldStorage()

# ---------------------------------------------------------------------------------------------------------------------

href = {None: ('Log In', 'login.py'), 0: ('Log In', 'login.py'), 1: ('Log Out', 'do_logout.py')}

print """
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta name="keywords" content="" />
<meta name="description" content="" />
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<title>WWAG Home</title>
<link href="css/home.css" rel="stylesheet" type="text/css" media="screen" />
</head>
<body>
"""
if (not loggedIn or not userType == 'S'):
    print """
<div id="header">
    <div id="navbar">
    <ul>
        <li><a href="{}" style="text-decoration:none;color:#fff">{}</a></li>
        <li><a href="aboutme.py" style="text-decoration:none;color:#fff">About Us</a></li>
        
        <li><a href="videos_search.py" style="text-decoration:none;color:#fff">Videos</a></li>
        <li><a href="home.py" style="text-decoration:none;color:#fff">Home</a></li>
              
    </ul>
    </div>
</div>
""".format(href[loggedIn][1], href[loggedIn][0])


else:
    
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
  
<body>
  <p>
    <div id="background">
    <img id ="image" src="http://flatlandgamestore.com/wp-content/uploads/2014/05/4513350626.jpg">
      <p id="text"> WWAG </p>
      <p id="text2"> The Wil Wheaton Appreciation Guild </p>
  </div>
  
  <div id="name">
    <p>WWWAG</p>
  </div>
    
"""


# If we passed a paramaeter do something
if foundParam == 1:
    if params['paramName'].value == "About":
        print """
            <h1>Welcome to the About Page</h1>
        """

            
# otherwise this is the 1st time we hit the page
else:
    
    # Just landed on the home page, nothing clicked yet.
    print """
        <h1>Welcome to our Sample Page - %s</h1>
    """ % sess.data.get('userName')



# Footer at the end
print """
    <p>This is the footer</p>
</body>
</html>
"""

# Tidy up and free resources
db.close()
sess.close()
