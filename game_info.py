# The libraries we'll need
import sys, cgi, redirect, session, MySQLdb

# Get the session and check if logged in
sess = session.Session(expires=60*20, cookie_path='/')
#loggedIn = sess.data.get('loggedIn')
form = cgi.FieldStorage()
db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003g29", "enigma29", "info20003g29", 3306)
# ---------------------------------------------------------------------------------------------------------------------
game_id = form.getvalue("game_id")
query = "SELECT * FROM Game WHERE GameID='{}'".format(game_id)
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
    An incorrect number of results ({}) were returned for the given game_id.
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
            <td>{}</td>
        </tr>
        <tr id='genre'>
            <td>Genre:</td>
            <td>{}</td>
        </tr>
        <tr id='cost'>
            <td>Cost:</td>
            <td>${}</td>
        </tr>
        <tr id='review_label'>
            <td colspan='2'>Review:</td>
        </tr>
        <tr id='review'>
            <td colspan='2'>{}</td>
        </tr>
        <tr id='star_rating'>
            <td>We give it:</td>
            <td>{} out of 5</td>
        </tr>
        <tr id='class_rating'>
            <td>Rating:</td>
            <td>{}</td>
        </tr>
        <tr id='platform_notes_label'>
            <td colspan='2'>Platform Notes:</td>
        </tr>
        <tr id='platform_notes'>
            <td>{}</td>
        </tr>
     </table>
     """.format(info['GameName'],info['Genre'],info['Cost'],info['Review'],\
                info['StarRating'],info['ClassificationRating'],
                info['PlatformNotes'])
     #"".format(firstname+lastname,gamerhandle,role,email,profiledescription) 
    game_name = info['GameName']
# send session cookie
print "%s\nContent-Type: text/html\n" % (sess.cookie)

if not game_name:
    game_name = 'None'

print """
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta name="keywords" content="" />
<meta name="description" content="" />
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<title>WWAG Game: {}</title>
<link href="css/player_info.css" rel="stylesheet" type="text/css" media="screen" />
</head>
<body>
""".format(game_name)

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
