# The libraries we'll need
import sys, cgi, redirect, session, MySQLdb

# Get the session and check if logged in
sess = session.Session(expires=60*20, cookie_path='/')
#loggedIn = sess.data.get('loggedIn')
form = cgi.FieldStorage()
db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003g29", "enigma29", "info20003g29", 3306)
# ---------------------------------------------------------------------------------------------------------------------
username = form.getvalue("username")
query = "SELECT * FROM Player WHERE UserName='{}'".format(username)
try:
    db.query(query)
    res = db.store_result()
    rows = res.fetch_row(maxrows = 0, how = 1)
    assert(len(rows) == 1)
    info = rows[0]
    query_success = True
except AssertionError, e:
    query_success = False
    message = """
    <p id='select_error' class='error'>
    An incorrect number of results ({}) were returned for the given username.
    </p>
    """.format(len(rows))
except Exception, e:
    query_success = False
    message = """
    <p id='select_error' class='error'>
    Database error : {}
    </p>
    """.format(repr(e))

if not query_success:
    body = message
else:
    body = """
    <table>
        <tr id='name'>
            <td>Name:</td>
            <td>{} (a.k.a {})</td>
        </tr>
        <tr id='role'>
            <td>Role:</td>
            <td>{}</td>
        </tr>
        <tr id='email'>
            <td>Email:</td>
            <td>{}</td>
        </tr>
        <tr id='description'>
            <td colspan='2'>{}</td>
        </tr>
     </table>
     """.format(info["FirstName"]+' '+info["LastName"], info["UserName"], info["Role"], info["Email"], info["ProfileDescription"])
     #"".format(firstname+lastname,gamerhandle,role,email,profiledescription) 
# send session cookie
print "%s\nContent-Type: text/html\n" % (sess.cookie)

if not username:
    username = "None"

print """
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta name="keywords" content="" />
<meta name="description" content="" />
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<title>WWAG Player: {}</title>
<link href="css/player_info.css" rel="stylesheet" type="text/css" media="screen" />
</head>
<body>
""".format(username)

print """
<div id="header">
    <div id="navbar">
    <ul>
        <li><a href="login.py" style="text-decoration:none;color:#fff">Log In</a></li>
        <li><a href="aboutme.py" style="text-decoration:none;color:#fff">About Us</a></li>
        
        <li><a href="videos_search.py" style="text-decoration:none;color:#fff">Videos</a></li>
        <li><a href="home.py" style="text-decoration:none;color:#fff">Home</a></li>
              
    </ul>
    </div>
</div>
"""
if query_success:
    print body
else:
    print message
print """
</body>
</html>
 """    
