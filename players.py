# The libraries we'll need
import sys, cgi, session, MySQLdb, warnings, hashlib, uuid, sql, html
from xml.sax.saxutils import *

warnings.filterwarnings('error', category=MySQLdb.Warning)
# Get the session and check if logged in
sess = session.Session(expires=60*20, cookie_path='/')
loggedIn = sess.data.get('loggedIn')
userType = sess.data.get('userType')

# send session cookie
print "%s\nContent-Type: text/html\n" % (sess.cookie)

# get form data
form = cgi.FieldStorage()
# additional entity to replace in escape function
entities = {'"': '&quot;'} 

# ---------------------------------------------------------------------------------------------------------------------
# Only logged in users who are players can access this page
if (not loggedIn or not userType == 'S'):
    # redirect to home page
    print html.do_redirect("home.py")
    sess.close()   
    sys.exit(0)
# ---------------------------------------------------------------------------------------------------------------------
    
print html.make_head("video_modify.css", title="WWAG Player")

print html.make_navbar(loggedIn, userType)


print """
<div class="search_form">
<h2 class="header">PLAYERS</h2>
<form id="myForm" action="players.py" method="post">
    <fieldset id="search">
        <legend>Maintain Player</legend>
        
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
        <input type="submit" name="submit" value="Search" onClick="DoSubmit()" />
    </div>
</form>
</div>
"""

####### CONNECT TO DATABASE AND LOAD FORM DATA ##########################################################################

db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003g29", "enigma29", "info20003g29", 3306)
cursor = db.cursor()
table = "Player"
keys = ['PlayerID', 'SupervisorID', 'FirstName', 'LastName', 'Role', 'PlayerType', 'ProfileDescription', 'Email', 'UserName', 'HashedPassword', 'Salt', 'Phone', 'VoiP']
exact_keys = ['PlayerID', 'SupervisorID']
ignore = ['HashedPassword', 'Salt']

fields = dict.fromkeys(keys)

for key in fields:
    fields[key] = form.getvalue(key)       

######## If INSERT button is pressed then ... ###########################################################################
if form.getvalue("submit") == "Insert":
    
    fields['Salt'] = uuid.uuid4().hex
    if fields["HashedPassword"] != None:
        fields["HashedPassword"] = hashlib.sha512(fields['HashedPassword'] + fields['Salt']).hexdigest()
    else:
        print '<div class = "error">Insert Error! Password is empty.</div>'
        sys.exit(0);
        print html.end_html
          
    print sql.insert(db, cursor, table, fields, keys)
    

####### GENERATE AND EXECUTE SEARCH QUERY  ################################################################################

result =  sql.search(db, cursor, table, fields, keys, exact_keys, select=["PlayerID", "UserName"], ignore=ignore, limit=10)
rows = result[0];
print result[1]; 
    
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
        print '<td><a href="player.py?PlayerID={0}">{0}</a></td><td><a href="player.py?PlayerID={0}">{1}</a></td>'.format(escape(str(row[0])), escape(str(row[1])))
        print '</tr>'
                                                                                             
print '</table>'    
                                                                                         
print html.end_html
                     
# Tidy up and free resources
cursor.close()
db.close()
sess.close()                                                                                        
