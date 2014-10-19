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
    
print html.make_head("video_modify.css", title="WWAG Video")

print html.make_navbar(loggedIn, userType)

print """
<div class="search_form">
<h2 class="header">VIDEOS</h2>
<form id = "myForm" action="videos_modify.py" method="post">
    <fieldset id="search">
        <legend>Maintain Video</legend>
        

        <div class="textbox">
            <label for="VideoID">Video ID:</label>
            <input name="VideoID" id="VideoID" type="text" />
        </div>

        <div class="textbox">
            <label for="VideoName">Video Name:</label>
            <input name="VideoName" id="VideoName" type="text" />
        </div>
        
         <div class="textbox">
            <label for="GameID">Game ID:</label>
            <input name="GameID" id="GameID" type="text" />
        </div>

        <div class="textbox">
            <label for="InstanceRunID">InstanceRun ID:</label>
            <input name="InstanceRunID" id="InstanceRunID" type="text" />
        </div>

         <div class="textbox">
            <label for="Price">Price:</label>
            <input name="Price" id="Price" type="text" />
        </div>

        <div class="textbox">
            <label for="VideoType">Video Type:</label>
            <input name="VideoType" id="VideoType" type="text" />
        </div>

        <div class="textbox">
            <label for="URL">URL:</label>
            <input name="URL" id="URL" type="text" />
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
table = "Video"
keys = ['VideoID', 'VideoName', 'URL', 'Price', 'VideoType', 'InstanceRunID', 'GameID']
exact_keys = ['VideoID', 'Price', 'InstanceRunID', 'GameID']
pk = ['VideoID']
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
        print '<form action="videos_modify.py" method="post">'
        i = 0
        print '<td><input name="VideoID" id="VideoID" type="hidden" value = "{0}" /><a href="video.py?video_id={0}">{0}</a></td>'.format(row[i])
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
sess.close()

