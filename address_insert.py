# The libraries we'll need
import sys, cgi, redirect, session, MySQLdb, warnings

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
# Only logged in users who are players can access this page

redirect_now = False
if form.getvalue('PlayerID') != None:
    table = 'Player'
    id = form.getvalue('PlayerID')
elif form.getvalue('ViewerID') != None:
    table = 'Viewer'
    id = form.getvalue('ViewerID')
else:
    redirect_now = True

if (not loggedIn or not userType == 'S') or (redirect_now == True):
    # redirect to home page
    print """\
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <meta http-equiv="refresh" content="0;url=%s">
    </head>
    <body>
    </body>
    """ % redirect.getQualifiedURL("/~mskh/dbsys/dbs2014sm2group29/home.py")
    sess.close()   
    sys.exit(0)

# ---------------------------------------------------------------------------------------------------------------------

print """
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta name="keywords" content="" />
<meta name="description" content="" />
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<title>WWAG Address</title>
<link href="css/video_modify.css" rel="stylesheet" type="text/css" media="screen" />
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
# ---------------------------------------------------------------------------------------------------------------------
####### CONNECT TO DATABASE ##########################################################################

db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003g29", "enigma29", "info20003g29", 3306)
cursor = db.cursor()
keys = ['AddressID', 'StreetNumber', 'StreetNumberSuffix', 'StreetName', 'StreetType', 'AddressType', 'AddressTypeIdentifier', 'MinorMunicipality', 'MajorMunicipality', 'GoverningDistrict', 'PostalArea', 'Country']
keys_a = ['{}ID'.format(table), 'AddressID', 'StartDate', 'EndDate']

fields = dict.fromkeys(keys + ['{}ID'.format(table), 'StartDate', 'EndDate'])

for key in fields:
    fields[key] = 'DEFAULT'          

for key in fields:
    if form.getvalue(key) != None:
        fields[key] = "'" + form.getvalue(key) + "'"
   
          
####### PRINT FORM ##############################################################################

print """
<div class="search_form">
<h2 class="header">ADDRESS</h2>
<form action="address_insert.py" method="post">
    <fieldset id="search">
        <legend>New Address</legend>
        
        <div class="textbox">
            <label for="{0}ID">{0}ID:</label>
            <input name="{0}ID" id="{0}ID" type="hidden" value = "{1}"/>
            <span class = "just_text">{1}</span>
        </div>

        <div class="textbox">
            <label for="AddressID">Address ID:</label>
            <input name="AddressID" id="AddressID" type="text"/>
        </div>

        <div class="textbox">
            <label for="StartDate">Start Date:</label>
            <input name="StartDate" id="StartDate" type="date"/>
        </div>

        <div class="textbox">
            <label for="EndDate">End Date:</label>
            <input name="EndDate" id="EndDate" type="date"/>
        </div>

        <div class="textbox">
            <label for="StreetNumber">Street Number:</label>
            <input name="StreetNumber" id="StreetNumber" type="text"/>
        </div>
        
         <div class="textbox">
            <label for="StreetNumberSuffix">StreetNumber Suffix :</label>
            <input name="StreetNumberSuffix" id="StreetNumberSuffix" type="text"/>
        </div>
        
        <div class="textbox">
            <label for="StreetName">Street Name:</label>
            <input name = "StreetName" id= "StreetName" type="text"/>
        </div>

        <div class="textbox">
            <label for="StreetType">Street Type:</label>
            <input name="StreetType" id="StreetType" type="text"/>
        </div>

        <div class="textbox">
            <label for="AddressType">Address Type:</label>
            <input name="AddressType" id="AddressType" type="text"/>
        </div>
        
        <div class="textbox">
            <label for="AddressTypeIdentifier">Address Type Identifier:</label>
            <input name="AddressTypeIdentifier" id="AddressTypeIdentifier" type="text" />
        </div>
        
        <div class="textbox">
            <label for="MinorMunicipality">Minor Municipality:</label>
            <input name="MinorMunicipality" id="MinorMunicipality" type="text"/>
        </div>

        <div class="textbox">
            <label for="MajorMunicipality">Major Municipality:</label>
            <input name="MajorMunicipality" id="MajorMunicipality" type="text"/>
        </div>

        <div class="textbox">
            <label for="GoverningDistrict">Governing District:</label>
            <input name="GoverningDistrict" id="GoverningDistricte" type="text"/>
        </div>

        <div class="textbox">
            <label for="PostalArea">Postal Area:</label>
            <input name="PostalArea" id="PostalArea" type="text"/>
        </div>

        <div class="textbox">
            <label for="Country">Country:</label>
            <input name="Country" id="Country" type="text"/>
        </div>
    </fieldset>
    
    <div id="buttons" class="button_select">
        <input type="reset" value="Reset" />
        <input type="submit" name="submit" value="Insert" />
    </div>
</form>
</div>
""".format(table, id)

​
######## If INSERT button is pressed then ... ###########################################################################
if form.getvalue("submit") == "Insert":

    #insert query is generated and there is an attempt to execute the query
    query = '''INSERT INTO Address VALUES ('''
    for key in keys:
        query += "{}, ".format(fields[key])
    query = query[:-2] + ");"

    try:   
        cursor.execute(query)
        db.commit()
    except Exception, e:
        print '<div class = "error">Insert Error! {}.</div>'.format(repr(e))
        sys.exit(0)
        
    if fields[keys[0]] == 'DEFAULT':
        fields[keys[0]] = 'LAST_INSERT_ID()'
        
    query = '''INSERT INTO {}Address VALUES ('''.format(table)
    for key in keys_a:
        query += "{}, ".format(fields[key])
    query = query[:-2] + ");"

    try:       
        cursor.execute(query)
        db.commit()
        print '<div class = "success">Insert Successful!</div>'
    except Exception, e:
        db.rollback()
        print '<div class = "error">Insert Error! {}.</div>'.format(repr(e))  ​​​
