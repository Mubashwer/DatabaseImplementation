# The libraries we'll need
import sys, cgi, redirect, session, MySQLdb

# Get the session and check if logged in
sess = session.Session(expires=60*20, cookie_path='/')

form = cgi.FieldStorage()
db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003g29", "enigma29", "info20003g29", 3306)
# ---------------------------------------------------------------------------------------------------------------------
mnm = form.getvalue("mnm")
#ModelAndMake: mnm
query = "SELECT * FROM Equipment WHERE ModelAndMake='{}'".format(mnm)
try:
    db.query(query)
    res = db.store_result()
    rows = res.fetch_row(maxrows = 0, how = 1)
    assert(len(rows) > 0)
    query_success = True
except AssertionError, e:
    query_success = False
    message = """
    <p id='select_error' class='error'>
    No results were returned for the given model and make.
    </p>
    """
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
        <tr id='mnm'>
            <td>Model and make:</td>
            <td>{}</td>
        </tr>
        <tr id='pspeed'>
            <td>Processor speed:</td>
            <td>{}</td>
        </tr>
        <tr id='reviewlabel'>
            <td colspan='2'>Review(s):</td>
        </tr>
    """.format(rows[0]["ModelAndMake"], rows[0]["ProcessorSpeed"])
    for result in rows:
        body += """
        <tr class = 'review'>
            <td colspan='2'>{}</td>
        </tr>
         """.format(result["EquipmentReview"])
    body += """
    </table>
    """
    
# send session cookie
print "%s\nContent-Type: text/html\n" % (sess.cookie)

if not mnm:
    mnm = "None"

print """
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta name="keywords" content="" />
<meta name="description" content="" />
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<title>WWAG Equipment: {}</title>
<link href="css/player_info.css" rel="stylesheet" type="text/css" media="screen" />
</head>
<body>
""".format(mnm)

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
