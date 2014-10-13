# The libraries we'll need
import sys, cgi, redirect, session, MySQLdb, warnings, hashlib, uuid

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
if(not loggedIn or not userType == 'S'):
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

print """
<div class="search_form">
<h2 class="header">PLAYERS</h2>
<form action="players.py" method="post">
    <fieldset id="search">
        <legend>Search Player</legend>
        
        <div class="textbox">
            <label for="PlayerID">Player ID:</label>
            <input name="PlayerID" id="PlayerID" type="text" />
        </div>

        <div class="textbox">
            <label for="SupervisorID">Supervisor ID:</label>
            <input name="SupervisorID" id="SupervisorID" type="text" />
        </div>
        
         <div class="textbox">
            <label for="FirstName">First Name :</label>
            <input name="FirstName" id="FirstName" type="text" />
        </div>
        
        <div class="textbox">
            <label for="LastName">Last Name:</label>
            <input name = "LastName" id= "LastName" type="text" />
        </div>

        <div class="textbox">
            <label for="Role">Role:</label>
            <input name="Role" id="Role" type="text" />
        </div>

        <div class="textbox">
            <label for="PlayerType">Player Type:</label>
            <input name="PlayerType" id="PlayerType" type="text" />
        </div>
        
        <div class="textbox">
            <label for="Player Type">UserName:</label>
            <input name="UserName" id="UserName" type="text" />
        </div>

        <div class="textbox">
            <label for="HashedPassword">Password:</label>
            <input name="HashedPassword" id="HashedPassword" type="text" />
        </div>

        <div class="textbox">
            <label for="Email">Email:</label>
            <input name="Email" id="Email" type="text" />
        </div>

        <div class="textbox">
            <label for="Phone">Phone:</label>
            <input name="Phone" id="Phone" type="text" />
        </div>

        <div class="textbox">
            <label for="VoiP ">Skype:</label>
            <input name="VoiP" id="VoiP" type="text" />
        </div>

        <div class="textbox2">
            <label for="Password ">Description:</label>
            <textarea name="ProfileDescription" id="ProfileDescription" cols="60" rows="5"></textarea>
        </div>
    </fieldset>
    
    <div id="buttons" class="button_select">
        <input type="reset" value="Reset" />
        <input type="submit" name="submit" value="Insert" />
        <input type="submit" name="submit" value="Search" />
    </div>
</form>
</div>
"""

####### CONNECT TO DATABASE AND LOAD FORM DATA ##########################################################################

db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003g29", "enigma29", "info20003g29", 3306)
cursor = db.cursor()
keys = ['PlayerID', 'SupervisorID', 'FirstName', 'LastName', 'Role', 'PlayerType', 'ProfileDescription', 'Email', 'UserName', 'HashedPassword', 'Salt', 'Phone', 'VoiP']
fields = dict.fromkeys(keys)

for key in fields:
    fields[key] = 'DEFAULT'        

for key in fields:
    if form.getvalue(key) != None:
        fields[key] = "'" + form.getvalue(key) + "'"        

######## If INSERT button is pressed then ... ###########################################################################
if form.getvalue("submit") == "Insert":

    #insert query is generated and there is an attempt to execute the query
    query = '''INSERT INTO Player VALUES ('''
    
    fields['Salt'] = uuid.uuid4().hex
    if fields["HashedPassword"] != 'DEFAULT':
        fields["HashedPassword"] = hashlib.sha512(form.getvalue('HashedPassword') + fields['Salt']).hexdigest()
    else:
        print '<div class = "error">Insert Error! Password is empty.</div>'
        sys.exit(0);
    
    fields['Salt'] = "'" + fields['Salt'] + "'"
    fields['HashedPassword'] = "'" + fields['HashedPassword'] + "'"
    
    for key in keys:
        query += "{}, ".format(fields[key])
    
    query = query[:-2] + ");"

    try:   
        cursor.execute(query)
        db.commit()
        print '<div class = "success">Insert Successful!</div>'
    except Exception, e:
        print '<div class = "error">Insert Error! {}.</div>'.format(repr(e)) 

####### GENERATE AND EXECUTE SEARCH QUERY  ################################################################################

query = "SELECT PlayerID, UserName FROM Player LIMIT 10;"
condition = "WHERE "
has_condition = False
                                                                                         
for key in fields:
    if fields[key] != 'DEFAULT':
        if key in ['PlayerID', 'SupervisorID']:
            condition += "{} = {} AND ".format(key, fields[key])
        elif key in ['HashedPassword', 'Salt']:
            continue         
        else:
            condition += "{} LIKE '%{}%' AND ".format(key, form.getvalue(key))                                                                                          
        has_condition = True
                                                                                          
                                                                                         
if has_condition:
    query = query[:-9] + condition[:-4] + "LIMIT 10;"                                                                                                                                                                              

rows = None    
try:   
    cursor.execute(query)
    rows = cursor.fetchall()
except Exception, e:   
    print '<div class = "error">Search Error! {}.</div>'.format(repr(e))
    
####### DISPLAY RESULTS TABLE  #############################################################################################
print '<table class="gridtable" align="center">'

# Print column headers    
print '<tr>'
print '<th>PlayerID</th><th>UserName</th>'
print '</tr>'

# Print each row of table    
if rows != None: 
    for row in rows:
        print '<tr>'
        print '<td><a href="player.py?PlayerID={0}">{0}</a></td><td><a href="player.py?PlayerID={0}">{1}</a></td>'.format(row[0], row[1])
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
