# The libraries we'll need
import sys, cgi, redirect, session, MySQLdb, warnings, hashlib, uuid

warnings.filterwarnings('error', category=MySQLdb.Warning)
# Get the session and check if logged in
sess = session.Session(expires=60*20, cookie_path='/')
loggedIn = sess.data.get('loggedIn')
userType = sess.data.get('userType')
userName = sess.data.get('userName')

# send session cookie
print "%s\nContent-Type: text/html\n" % (sess.cookie)

# get form data
form = cgi.FieldStorage()

# ---------------------------------------------------------------------------------------------------------------------
# Only logged in users who are players can access this page
if 0 == 1 and (not loggedIn or not userType == 'S'):
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
####### CONNECT TO DATABASE LOAD PLAYER DATA ##########################################################################

db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003g29", "enigma29", "info20003g29", 3306)
cursor = db.cursor()
keys = ['PlayerID', 'SupervisorID', 'FirstName', 'LastName', 'Role', 'PlayerType', 'ProfileDescription', 'Email', 'UserName', 'HashedPassword', 'Salt', 'Phone', 'VoiP', 'AddressID', 'StartDate', 'EndDate']
fields = dict.fromkeys(keys)
message = "";

if form.getvalue(keys[0]) == None:
    querySearch = "SELECT * FROM Player WHERE UserName = '{}';".format(userName)
else:
    querySearch = "SELECT * FROM Player WHERE PlayerID = '{}';".format(form.getvalue(keys[0])) 

for key in fields:
    fields[key] = 'DEFAULT'          

for key in fields:
    if form.getvalue(key) != None:
        fields[key] = "'" + form.getvalue(key) + "'"

######## If UPDATE button is pressed then ... ############################################################################
ignore_password = 0;
if form.getvalue("submit") == "Update":        
    query = "UPDATE Player SET "
    
    fields['Salt'] = uuid.uuid4().hex
    if (fields["HashedPassword"] == 'DEFAULT'):
        ignore_password = 1;
    else:
        fields["HashedPassword"] = hashlib.sha512(form.getvalue('HashedPassword') + fields['Salt']).hexdigest()
    
    
    fields['Salt'] = "'" + fields['Salt'] + "'"
    fields['HashedPassword'] = "'" + fields['HashedPassword'] + "'"
    
    for key in keys[:-3]:
        if(ignore_password == 1 and key == "HashedPassword"):
            continue;
        query += "{} = {}, ".format(key, fields[key])
        
    query = query[:-2] + " WHERE PlayerID = {};".format(fields[keys[0]])
    
    try:   
        cursor.execute(query)
        db.commit()
        message =  '<div class = "success">Update Successful!</div>'
    except Exception, e:
        message =  '<div class = "error">Update Error! {}.</div>'.format(repr(e))
        
######## If DELETE button is pressed then ... ###########################################################################        
if form.getvalue("submit") == "Delete":
    query = "DELETE FROM Player WHERE PlayerID = {};".format(fields[keys[0]])
    try:   
        cursor.execute(query)
        db.commit()
        message =  '<div class = "success">Delete Successful!</div>'
    except Exception, e:        
        message =  '<div class = "error">Delete Error! {}.</div>'.format(repr(e)) 
        
####### GENERATE AND EXECUTE SEARCH QUERY ##########################################################################
try:   
    cursor.execute(querySearch)
    row = cursor.fetchone()
except Exception, e:   
    print '<div class = "error">Search Error! {}.</div>'.format(repr(e))

if row == None:
    row = ["", "", "", "", "", "",  "", "", "", "", "", "",  ""]

row = list(row)
for i in range(13):
    if row[i] == None:
        row[i] = ""

####### PRINT FORM ##############################################################################
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

print """
<div class="search_form">
<h2 class="header">PLAYERS</h2>
<form action="player.py" method="post">
    <fieldset id="search">
        <legend>Maintain Player</legend>
        
        <div class="textbox">
            <label for="PlayerID">Player ID:</label>
            <input name="PlayerID" id="PlayerID" type="hidden" value = "{0}" />
            <span class = "just_text">{0}</span>
        </div>

        <div class="textbox">
            <label for="SupervisorID">Supervisor ID:</label>
            <input name="SupervisorID" id="SupervisorID" type="text" value = "{1}" />
        </div>
        
         <div class="textbox">
            <label for="FirstName">First Name :</label>
            <input name="FirstName" id="FirstName" type="text" value = "{2}" />
        </div>
        
        <div class="textbox">
            <label for="LastName">Last Name:</label>
            <input name = "LastName" id= "LastName" type="text" value = "{3}" />
        </div>

        <div class="textbox">
            <label for="Role">Role:</label>
            <input name="Role" id="Role" type="text" value = "{4}" />
        </div>

        <div class="textbox">
            <label for="PlayerType">Player Type:</label>
            <input name="PlayerType" id="PlayerType" type="text" value = "{5}" />
        </div>
        
        <div class="textbox">
            <label for="Player Type">UserName:</label>
            <input name="UserName" id="UserName" type="text" value = "{8}" />
        </div>
        
        <div class="textbox">
            <label for="HashedPassword">Password:</label>
            <input name="HashedPassword" id="HashedPassword" type="text" />
        </div>

        <div class="textbox">
            <label for="Email">Email:</label>
            <input name="Email" id="Email" type="text" value = "{7}" />
        </div>

        <div class="textbox">
            <label for="Phone">Phone:</label>
            <input name="Phone" id="Phone" type="text" value = "{11}"/>
        </div>

        <div class="textbox">
            <label for="VoiP ">Skype:</label>
            <input name="VoiP" id="VoiP" type="text" value = "{12}"/>
        </div>

        <div class="textbox2">
            <label for="Password ">Description:</label>
            <textarea name="ProfileDescription" id="ProfileDescription" cols="60" rows="5" value = "{6}">{6}</textarea>
        </div>
    </fieldset>
    
    <div id="buttons" class="button_select">
        <input type="reset" value="Reset" />
        <input type="submit" name="submit" value="Update" />
        <input type="submit" name="submit" value="Delete" />
    </div>
</form>
</div>
""".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12]) 

######## If DELETE ADDRESS button is pressed then ... ###########################################################################        
if form.getvalue("submit") == "Change":
    query = "UPDATE PlayerAddress SET AddressID = {0}, StartDate = {1}, EndDate = {2} WHERE PlayerID = {3};".format(fields[keys[-3]], fields[keys[-2]], fields[keys[-1]], fields[keys[0]])
    try:   
        cursor.execute(query)
        db.commit()
        message = '<div class = "success">Update Successful!</div>'
    except Exception, e:        
        message =  '<div class = "error">Update Error! {}.</div>'.format(repr(e))
        
######## If UPDATE ADDRESS button is pressed then ... ###########################################################################        
if form.getvalue("submit") == "DeleteAddress":
    query = "DELETE FROM PlayerAddress WHERE PlayerID = {1} AND AddressID = {0}; DELETE FROM Address WHERE AddressID = {0};".format(fields[keys[-3]], fields[keys[0]])
    try:   
        cursor.execute(query)
        db.commit()
        message =  '<div class = "success">Delete Successful!</div>'
    except Exception, e:        
        message = '<div class = "error">Delete Error! {}.</div>'.format(repr(e))        

####### GENERATE AND EXECUTE SEARCH QUERY FOR ADDRESS  ################################################################################

query = "SELECT AddressID, StartDate, EndDate FROM PlayerAddress WHERE PlayerID = {} ORDER BY StartDate DESC;".format(fields[keys[0]])

rows = None    
try:   
    cursor.execute(query)
    rows = cursor.fetchall()
except Exception, e:   
    message = '<div class = "error">Search Error! {}.</div>'.format(repr(e))

    
####### DISPLAY RESULTS TABLE  #############################################################################################
print message
print '''<div class="insert_button"><input type="button" onClick="parent.location='address_insert.py?PlayerID={}'" value='InsertAddress'></div>'''.format(form.getvalue(keys[0]))
print '<table class="gridtable" align="center">'

# Print column headers    
print '<tr>'
print "<th>AddressID</th><th>StartDate</th><th>EndDate</th><th>Change</th><th>Update</th><th>Delete</th>"
print '</tr>'

# Print each row of table    
if rows != None: 
    for row in rows:
        print '<tr>'
        print '<form action="player.py?PlayerID={}" method="post">'.format(form.getvalue(keys[0]))
        print '<td><input name="AddressID" id="AddressID" type="text" value ="{}" /></td>'.format(row[0])
        print '<td><input name="StartDate" id="StartDate" type="text" value ="{}" /></td>'.format(row[1])
        print '<td><input name="EndDate" id="EndDate" type="text" value ="{}" /></td>'.format(row[2])
        print '<td><input type="submit" name="submit" value="Change" /></td>'
        print '''<td><input type="button" onClick="parent.location='address_update.py?AddressID={}'" value='UpdateAddress'></td>'''.format(row[0])
        print '<td><input type="submit" name="submit" value="DeleteAddress" /></td>'
        print '</form>'
        print '</tr>'
                                                                                             
print '</table>'    
                                                                                         
print """
</body>
</html>
"""

# Tidy up and free resources
cursor.close()
db.close()
sess.close()
