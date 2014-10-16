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

####### LOAD FORM DATA ##########################################################################

db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003g29", "enigma29", "info20003g29", 3306)
cursor = db.cursor()
table = "Game"
keys = ['GameID', 'Genre', 'Review', 'StarRating', 'ClassificationRating', 'PlatformNotes', 'PromotionLink', 'Cost', 'GameName']
ignore = ['Genre', 'Review', 'StarRating', 'ClassificationRating', 'PlatformNotes', 'PromotionLink', 'Cost', 'GameName']
exact_keys = ['GameID', 'StarRating', 'Cost']
pk = ['GameID']

fields = dict.fromkeys(keys)
row = None
message = ""

for key in fields:
    fields[key] = form.getvalue(key)       

        
######## If INSERT button is pressed then ... ###########################################################################
if form.getvalue("submit") == "Insert":    
    message =  sql.insert(db, cursor, table, fields, keys)

######## If DELETE button is pressed then ... ###########################################################################        
if form.getvalue("submit") == "Delete":
    message =  sql.delete(db, cursor, table, fields, pk)
        
######## If UPDATE button is pressed then ... ############################################################################
if form.getvalue("submit") == "Update":        
    message =  sql.update(db, cursor, table, fields, keys, pk)        
        
######## LOAD RESULT ... ############################################################################
        
result =  sql.search(db, cursor, table, fields, keys, exact_keys, ignore=ignore, limit=10, fetch_one=True)
row = result[0];

if row == None:
    row = ["", "", "", "", "", "",  "", "", ""]

row = list(row)
for i in range(8):
    if row[i] == None:
        row[i] = ""
    else:
        row[i] = escape(str(row[i]), entities)   

####### PRINT FORM ##############################################################################
        
print """
<div class="search_form">
<h2 class="header">GAMES</h2>
<form name="myForm" id="myForm" action="games.py"  method="post">
    <fieldset id="search">
        <legend>Maintain Game</legend>
        
        <div class="textbox">
            <label for="GameID">Game ID:</label>
            <input name="GameID" id="GameID" type="text" value = "{0}" />
        </div>

        <div class="textbox">
            <label for="GameName">Game Name*:</label>
            <input name="GameName" id="GameName" type="text" value = "{8}" />
        </div>
        
         <div class="textbox">
            <label for="Genre">Genre :</label>
            <input name="Genre" id="Genre" type="text" value = "{1}" />
        </div>
        
        <div class="textbox">
            <label for="LastName">Star Rating:</label>
            <input name = "StarRating" id= "StarRating" type="text" value = "{3}" />
        </div>

        <div class="textbox">
            <label for="Cost">Cost:</label>
            <input name="Cost" id="Cost" type="text" value = "{7}" />
        </div>
        
        <div class="textbox">
            <label for="ClassificationRating">Classification Rating:</label>
            <input name="ClassificationRating" id="ClassificationRating" type="text" value = "{4}" />
        </div>

        <div class="textbox">
            <label for="PromotionLink">Promotion Link:</label>
            <input name="PromotionLink" id="PromotionLink" type="text" value = "{6}" />
        </div>

        <div class="textbox2">
            <label for="PlatformNotes ">Platform Notes:</label>
            <textarea name="PlatformNotes" id="PlatformNotes" cols="60" rows="5" value = "{5}">{5}</textarea>
        </div>

        <div class="textbox2">
            <label for="Review ">Review:</label>
            <textarea name="Review" id="Review" cols="60" rows="5" value = "{2}">{2}</textarea>
        </div>
    </fieldset>
    
    <div id="buttons" class="button_select">
        <input type="reset" value="Reset" />
        <input type="submit" name="submit" value="Insert"/>
        <input type="submit" name="submit" value="Search" onclick="DoSubmit()"/>
        <input type="submit" name="submit" value="Update" />
        <input type="submit" name="submit" value="Delete" />
    </div>
</form>
</div>
""".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]) 
 

####### GENERATE AND EXECUTE SEARCH QUERY  ################################################################################

result =  sql.search(db, cursor, table, fields, keys, exact_keys, select=["GameID", "GameName"], limit=10)
rows = result[0];
print result[1];    

    
####### DISPLAY RESULTS TABLE  #############################################################################################
print message
print '<table class="gridtable" align="center">'

# Print column headers    
print '<tr>'
print '<th>GameID</th><th>GameName</th>'
print '</tr>'

# Print each row of table    
if rows != None: 
    for a_row in rows:
        print '<tr>'
        print '<td><a href="games.py?GameID={0}">{0}</a></td><td><a href="games.py?GameID={0}">{1}</a></td>'.format(a_row[0], a_row[1])
        print '</tr>'
                                                                                             
print '</table>'    
                                                                                         
print html.end_html

# Tidy up and free resources
cursor.close()
db.close()
sess.close()                                                                                        
