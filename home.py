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
<link href="css/style.css" rel="stylesheet" type="text/css" media="screen" />
</head>
<body>
"""

# Main HTML content, starting with header and main menu
print """
    <h1><a href="home.py">Our Demo Page</a></h1>
    <ul>
        <li><a href="home.py">Main Page</a></li>
        <li><a href="home.py?paramName=About">About</a></li>
        %s
    </ul>
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
