# The libraries we'll need
import sys, cgi, redirect, session, MySQLdb, warnings, hashlib, uuid, sql, html
from xml.sax.saxutils import *

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



# ---------------------------------------------------------------------------------------------------------------------
####### CONNECT TO DATABASE LOAD PLAYER DATA ##########################################################################

db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003g29", "enigma29", "info20003g29", 3306)
table = 'Player'
cursor = db.cursor()
keys = ['PlayerID', 'SupervisorID', 'FirstName', 'LastName', 'Role', 'PlayerType', 'ProfileDescription', 'Email', 'UserName', 'HashedPassword', 'Salt', 'Phone', 'VoiP']
exact_keys = ['PlayerID', 'SupervisorID']
ignore = ['HashedPassword', 'Salt']
pk = ['PlayerID']
a_keys = ['AddressID', 'StreetNumber', 'StreetNumberSuffix', 'StreetName', 'StreetType', 'AddressType', 'AddressTypeIdentifier', 'MinorMunicipality', 'MajorMunicipality', 'GoverningDistrict', 'PostalArea', 'Country']
address_keys = ['PlayerID', 'AddressID', 'StartDate', 'EndDate']
address_exact = ['PlayerID', 'AddressID']
address_pk = ['PlayerID', 'AddressID', 'StartDate']

fields = dict.fromkeys(keys)
message = "";

for key in keys + address_keys:
    fields[key] = form.getvalue(key) 

######## If UPDATE button is pressed then ... ############################################################################
ignore_update = [];
if form.getvalue("submit") == "Update":        
    fields['Salt'] = uuid.uuid4().hex
    if fields["HashedPassword"] != None:
        fields["HashedPassword"] = hashlib.sha512(fields['HashedPassword'] + fields['Salt']).hexdigest()
    else:
        ignore_update = ignore
          
    message =  sql.update(db, cursor, table, fields, keys, pk, ignore=ignore_update)
        
######## If DELETE button is pressed then ... ###########################################################################        
if form.getvalue("submit") == "Delete":
    message =  sql.delete(db, cursor, table, fields, pk)
        
####### GENERATE AND EXECUTE SEARCH QUERY ##########################################################################
result =  sql.search(db, cursor, table, fields, keys, exact_keys, ignore=ignore, limit=10, fetch_one=True)
row = result[0];

if row == None:
    row = ["", "", "", "", "", "",  "", "", ""]

row = list(row)
for i in range(9):
    if row[i] == None:
        row[i] = ""
    else:
        row[i] = escape(str(row[i]), entities)   

####### PRINT FORM ##############################################################################
print message
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

######## If CHANGE ADDRESS (Date, ID) button is pressed then ... ###########################################################################        
if form.getvalue("submit") == "Change":
    print sql.update(db, cursor, "PlayerAddress", fields, address_keys, address_pk)
        
######## If DELETE ADDRESS button is pressed then ... ###########################################################################        
if form.getvalue("submit") == "DeleteAddress":
    print sql.delete(db, cursor, "PlayerAddress", fields, address_pk)
    print sql.delete(db, cursor, "Address", fields, ['AddressID'])
    
####### GENERATE AND EXECUTE SEARCH QUERY FOR ADDRESS  ################################################################################

result =  sql.search(db, cursor, "PlayerAddress", fields, address_keys, address_exact, select=["AddressID", "StartDate", "EndDate"], ignore=address_keys, order="ORDER BY StartDate DESC")
rows = result[0];
print result[1];

    
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
        print '<td><input name="AddressID" id="AddressID" type="hidden" value ="{0}" />{0}</td>'.format(row[0])
        print '<td><input name="StartDate" id="StartDate" type="hidden" value ="{0}" />{0}</td>'.format(escape(str(row[1]), entities))
        print '<td><input name="EndDate" id="EndDate" type="text" value ="{}" /></td>'.format(escape(str(row[2]), entities))
        print '<td><input type="submit" name="submit" value="Change" /></td>'
        print '''<td><input type="button" onClick="parent.location='address_update.py?AddressID={}'" value='UpdateAddress'></td>'''.format(row[0])
        print '<td><input type="submit" name="submit" value="DeleteAddress" /></td>'
        print '</form>'
        print '</tr>'
                                                                                             
print '</table>'    
                                                                                         
print html.end_html

# Tidy up and free resources
cursor.close()
db.close()
sess.close()
