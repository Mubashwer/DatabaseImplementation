import sys, cgi, redirect, session, MySQLdb, time
from common import *
from html import *

sess = session.Session(expires=60*20, cookie_path='/')
form = cgi.FieldStorage()

db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003g29", "enigma29", "info20003g29", 3306)
c=db.cursor()

attrs = ["VideoID", "ViewerOrderID", "OrderDate", "ViewedStatus", "ViewerID", "FlagPerk"]
vals = [None for attr in attrs]
data = dict(zip(attrs,vals))

data["VideoID"] = form.getvalue("video_id")
data["ViewerOrderID"] = "DEFAULT"
data["OrderDate"] = time.strftime("%Y-%m-%d")
data["ViewedStatus"] = False

username = sess.data.get("userName")
logged_in = sess.data.get("loggedIn")
user_type = sess.data.get("userType")
                              
if not logged_in or user_type in ['S']:
    print "Status: 307 Temporary Redirect"
    print "Location: login.py"

db.query("SELECT * FROM Viewer WHERE UserName = '{}'".format(username))
res = db.store_result()
rows = res.fetch_row(maxrows = 0, how = 1)

data["ViewerID"] = rows[0]["ViewerID"]

if user_type in ['C','B']:#TODO:any others?
    data["FlagPerk"] = 1
else:
    data["FlagPerk"] = 0

access_code = form.getvalue("access_code")
access_code_correct = False
if access_code:
    db.query("SELECT * FROM AccessCodeVideo WHERE VideoID = " + data["VideoID"])
    res = db.store_result()
    rows = res.fetch_row(maxrows = 0, how = 1)
    valid_codes = [row["AccessCodeID"] for row in rows]
    access_code_correct = (access_code in valid_codes)
head_injection = ''    
if access_code_correct or user_type in ['P','B']:
    access_granted = True
else:
    access_granted = False

if not access_granted:
    if data["VideoID"]:
        redirect_to = "video.py?video_id="+str(data["VideoID"])
    else:
        redirect_to = "videos_search.py"
    head_injection = '<meta http-equiv="refresh" content="5;url={}" />'.format(redirect_to)
            
print "%s\nContent-Type: text/html\n" % (sess.cookie)
     
print """
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
{}
<meta name="keywords" content="" />
<meta name="description" content="" />
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<title>WWAG: Order Confirmation</title>
<link href="css/login.css" rel="stylesheet" type="text/css" media="screen" />
</head>
<body>
<div id="greeting"><h2>Order</h2><div id = "message">
""".format(head_injection)

# Try to insert into the database, print the html body
try:
    assert(access_granted)
    #ViewerOrder:
    #(ViewerOrderID,OrderDate,ViewedStatus,ViewerID)
    c.execute("INSERT INTO ViewerOrder VALUES (DEFAULT,%s,%s,%s)",\
                    (data["OrderDate"],\
                     data["ViewedStatus"],\
                     data["ViewerID"]))
    #We need to get the ViewerOrderID that was just inserted, to match with the next query
    c.execute("SELECT ViewerOrderID FROM ViewerOrder ORDER BY ViewerOrderID DESC LIMIT 1")
    rows = results_as_dicts(c)
    data["ViewerOrderID"] = rows[0]["ViewerOrderID"]
    
    #ViewerOrderLine:
    #(VideoID,ViewerOrderID,,FlagPerk)
    c.execute("INSERT INTO ViewerOrderLine VALUES (%s,%s,%s)",\
                    (data["VideoID"],\
                     data["ViewerOrderID"],\
                     data["FlagPerk"]))
    db.commit()
    print """
    <p id='success'>
        Your order request has been successfully processed.  Thankyou for using WWAG online.
    </p>
    """
except AssertionError:
        print """
        <p id='access_denied' class='error'>
            {}<br/>
            {}<br/>
            Sorry, access has not been granted.  Redirecting...
        </p>
        """.format(access_granted,valid_codes)
except MySQLdb.Error, e:
        print """
        <p id='mysql_error' class='error'>
            Sorry, has been an error in our database: 
            <br/>
            {}
        </p>
        """.format(e)
        db.rollback()
except Exception, e:
        print """
        <p id='unexpected_error' class='error'>
            Sorry, an unexpected error has occured:
            <br/>
            {}
        </p>
        """.format(e)
                                    
print """
</div></div?
</body>
</html>
"""
