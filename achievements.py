# The libraries we'll need
import sys, cgi, redirect, session, MySQLdb, warnings, sql, html
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
    
print html.make_head("video_modify.css", title="WWAG Achievements")

print html.make_navbar(loggedIn, userType)

print """
<div class="search_form">
<h2 class="header">ACHIEVEMENTS</h2>
<form id="myForm" action="achievements.py" method="post">
    <fieldset id="search">
        <legend>Maintain Achievement</legend>
        
        <div class="textbox">
            <label for="AchievementID">Achievement ID:</label>
            <input name="AchievementID" id="AchievementID" type="text" />
        </div>
        
        <div class="textbox">
            <label for="InstanceRunID">Instance Run ID:</label>
            <input name="InstanceRunID" id="InstanceRunID" type="text" />
        </div>
        
        <div class="textbox">
            <label for="WhenAchieved">Achievement Time:</label>
            <input name = "WhenAchieved" id= "WhenAchieved" type="datetime-local" step=1>
        </div>

        <div class="textbox">
            <label for="AchievementName">Achievement Name:</label>
            <input name="AchievementName" id="AchievementName" type="text" />
        </div>

        <div class="textbox">
            <label for="RewardBody">Reward Body:</label>
            <input name="RewardBody" id="RewardBody" type="text" />
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
table = "Achievement"
keys = ['AchievementID', 'InstanceRunID', 'WhenAchieved', 'AchievementName', 'RewardBody']
exact_keys = ['AchievementID', 'InstanceRunID', 'WhenAchieved']
pk = ['AchievementID']
fields = dict.fromkeys(keys)

for key in fields:
    fields[key] = form.getvalue(key) 


######## If INSERT button is pressed then ... ###########################################################################
if form.getvalue("submit") == "Insert":    
    print sql.insert(db, cursor, table, fields, keys)

######## If DELETE button is pressed then ... ###########################################################################        
if form.getvalue("submit") == "Delete":
    print sql.delete(db, cursor, table, fields, pk)
        
######## If UPDATE button is pressed then ... ############################################################################
if form.getvalue("submit") == "Update":        
    print sql.update(db, cursor, table, fields, keys, pk) 
    
####### GENERATE AND EXECUTE SEARCH QUERY  ################################################################################
result =  sql.search(db, cursor, table, fields, keys, exact_keys, limit=10)
rows = result[0];
print result[1]; 
            

####### DISPLAY RESULTS TABLE  #############################################################################################
print '<table class="gridtable" align="center">'

# Print column headers    
print '<tr>'
for key in keys:
    print '<th>{}</th>'.format(key)
print '<th>Update</th><th>Delete</th>'
print '</tr>'

# Print each row of table    
if rows != None: 
    for row in rows:
        print '<tr>'
        print '<form action="achievements.py" method="post">'
        i = 0
        print '<td><input name="AchievementID" id="AchievementID" type="hidden" value = "{0}" />{0}</td>'.format(row[i])
        i += 1
        # Print each field of row as textbox
        for key in keys[1:]:
            if row[i] == None:
                field = ''
            else:
                field = row[i]
            print '<td><span class="row_textbox"><input name="{0}" id="{0}" type="text" value = "{1}" /></span></td>'.format(key, escape(str(field), entities))
            i += 1
        print '<td><input type="submit" name="submit" value="Update" /></td><td><input type="submit" name="submit" value="Delete" /></td>'
        print '</form>'
        print '</tr>'
                                                                                             
print '</table>'    
                                                                                         
print html.end_html

# Tidy up and free resources
cursor.close()
db.close()
sess.close()                                                                                        










