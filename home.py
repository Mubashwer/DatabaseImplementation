# The libraries we'll need
import sys, session, cgi, MySQLdb

# Get a DB connection
db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003", "cisds", "info20003", 3306)
cursor = db.cursor()

# What came on the URL string?
params = cgi.FieldStorage()

foundParam=0

# Check if the parameter we are looking for was passed
if params.has_key('paramName'):

    foundParam=1

# Manage the session
sess = session.Session(expires=20*60, cookie_path='/')

# send session cookie
print "%s\nContent-Type: text/html\n" % (sess.cookie)
    
# Send head of HTML document, pointing to our style sheet
print """
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta name="keywords" content="" />
<meta name="description" content="" />
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<title>Sample Page</title>
<link href="css/home.css" rel="stylesheet" type="text/css" media="screen" />
</head>
<body>
"""

# Main HTML content, starting with header and main menu
print """
    <div id="header">
			<div id="navbar">
				<ul>
            <li><a href="home.py" style="text-decoration:none;color:#fff">Home</a></li>
            <li><a href="Aboutme.py" style="text-decoration:none;color:#fff">About Us</a></li>
            <li><a href="logout.py" style="text-decoration:none;color:#fff">Log Out</a></li>
            <li><a href="video_search.py" style="text-decoration:none;color:#fff">Videos</a>
              <ul>
						<li><a href="#" style="text-decoration:none;color:#fff">Video 1</a></li>
						<li><a href="#" style="text-decoration:none;color:#fff">Video 2</a></li>
                <li><a href="#" style="text-decoration:none;color:#fff">Video 3</a></li>
					</ul>
          </li>
              
				</ul>
			</div>
			
		</div>
  
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
    
""" % ( "<li><a href=\"do_logout.py\"><font color=red>Logout</font></a></li>" if sess.data.get('loggedIn') else "<li><a href=\"login.py\">Login</a></li>")

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
