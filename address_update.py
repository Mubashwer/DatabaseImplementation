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
if (not loggedIn or not userType == 'S'):
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
<title>WWAG Players</title>
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
####### CONNECT TO DATABASE LOAD PLAYER DATA ##########################################################################

db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003g29", "enigma29", "info20003g29", 3306)
cursor = db.cursor()
keys = ['AddressID', 'StreetNumber', 'StreetNumberSuffix', 'StreetName', 'StreetType', 'AddressType', 'AddressTypeIdentifier', 'MinorMunicipality', 'MajorMunicipality', 'GoverningDistrict', 'PostalArea', 'Country']
fields = dict.fromkeys(keys)

querySearch = "SELECT * FROM Address WHERE AddressID = '{}';".format(form.getvalue(keys[0]))

for key in fields:
    fields[key] = 'DEFAULT'          

for key in fields:
    if form.getvalue(key) != None:
        fields[key] = "'" + form.getvalue(key) + "'"
message = ""

######## If UPDATE button is pressed then ... ############################################################################
if form.getvalue("submit") == "Update":        
    query = "UPDATE Address SET "
    for key in keys:
        query += "{} = {}, ".format(key, fields[key])
        
    query = query[:-2] + " WHERE AddressID = {};".format(fields[keys[0]])
    
    try:   
        cursor.execute(query)
        db.commit()
        message =  '<div class = "success">Update Successful!</div>'
    except Exception, e:
        message =  '<div class = "error">Update Error! {}.</div>'.format(repr(e))

        
####### GENERATE AND EXECUTE SEARCH QUERY ##########################################################################
row = None
try:   
    cursor.execute(querySearch)
    row = cursor.fetchone()
except Exception, e:   
    print '<div class = "error">Search Error! {}.</div>'.format(repr(e))

if row == None:
    row = ["", "", "", "", "", "",  "", "", "", "", "", ""]

row = list(row)
for i in range(12):
    if row[i] == None:
        row[i] = ""

####### PRINT FORM ##############################################################################

print """
<div class="search_form">
<h2 class="header">ADDRESS</h2>
<form action="address_update.py" method="post">
    <fieldset id="search">
        <legend>Maintain Address</legend>
        
        <div class="textbox">
            <label for="AddressID">Address ID:</label>
            <input name="AddressID" id="AddressID" type="hidden" value = "{0}" />
            <span class = "just_text">{0}</span>
        </div>

        <div class="textbox">
            <label for="StreetNumber">Street Number:</label>
            <input name="StreetNumber" id="StreetNumber" type="text" value = "{1}" />
        </div>
        
         <div class="textbox">
            <label for="StreetNumberSuffix">StreetNumber Suffix :</label>
            <input name="StreetNumberSuffix" id="StreetNumberSuffix" type="text" value = "{2}" />
        </div>
        
        <div class="textbox">
            <label for="StreetName">Street Name:</label>
            <input name = "StreetName" id= "StreetName" type="text" value = "{3}" />
        </div>

        <div class="textbox">
            <label for="StreetType">Street Type:</label>
            <input name="StreetType" id="StreetType" type="text" value = "{4}" />
        </div>

        <div class="textbox">
            <label for="AddressType">Address Type:</label>
            <input name="AddressType" id="AddressType" type="text" value = "{5}" />
        </div>
        
        <div class="textbox">
            <label for="AddressTypeIdentifier">Address Type Identifier:</label>
            <input name="AddressTypeIdentifier" id="AddressTypeIdentifier" type="text" value = "{6}" />
        </div>
        
        <div class="textbox">
            <label for="MinorMunicipality">Minor Municipality:</label>
            <input name="MinorMunicipality" id="MinorMunicipality" type="text" value = "{7}"/>
        </div>

        <div class="textbox">
            <label for="MajorMunicipality">Major Municipality:</label>
            <input name="MajorMunicipality" id="MajorMunicipality" type="text" value = "{8}" />
        </div>

        <div class="textbox">
            <label for="GoverningDistrict">Governing District:</label>
            <input name="GoverningDistrict" id="GoverningDistricte" type="text" value = "{9}"/>
        </div>

        <div class="textbox">
            <label for="PostalArea">Postal Area:</label>
            <input name="PostalArea" id="PostalArea" type="text" value = "{10}"/>
        </div>

        <div class="textbox">
            <label for="Country">Country:</label>
            <input name="Country" id="Country" type="text" value = "{11}"/>
        </div>
    </fieldset>
    
    <div id="buttons" class="button_select">
        <input type="reset" value="Reset" />
        <input type="submit" name="submit" value="Update" />
    </div>
</form>
</div>
""".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]) 

print message
