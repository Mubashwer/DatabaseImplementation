# The libraries we'll need
import sys, cgi, redirect, session, MySQLdb, warnings, sql, html

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

redirect_now = False
if form.getvalue('PlayerID') != None:
    table = 'Player'
    id = form.getvalue('PlayerID')
elif form.getvalue('ViewerID') != None:
    table = 'Viewer'
    id = form.getvalue('ViewerID')
else:
    redirect_now = True

# ---------------------------------------------------------------------------------------------------------------------
# Only logged in users who are players can access this page
if (not loggedIn or not userType == 'S') or (redirect_now == True):
    # redirect to home page
    print html.do_redirect("home.py")
    sess.close()   
    sys.exit(0)

# ---------------------------------------------------------------------------------------------------------------------
    
print html.make_head("video_modify.css", title="WWAG Address")

print html.make_navbar(loggedIn, userType)
# ---------------------------------------------------------------------------------------------------------------------
####### CONNECT TO DATABASE ##########################################################################

db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003g29", "enigma29", "info20003g29", 3306)
cursor = db.cursor()
keys = ['AddressID', 'StreetNumber', 'StreetNumberSuffix', 'StreetName', 'StreetType', 'AddressType', 'AddressTypeIdentifier', 'MinorMunicipality', 'MajorMunicipality', 'GoverningDistrict', 'PostalArea', 'Country']
keys_a = ['{}ID'.format(table), 'AddressID', 'StartDate', 'EndDate']

fields = dict.fromkeys(keys + keys_a)

for key in fields:
    fields[key] = form.getvalue(key)

          
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


######## If INSERT button is pressed then ... ###########################################################################
if form.getvalue("submit") == "Insert":

    print sql.insert(db, cursor, "Address", fields, keys)
    if(fields['AddressID'] == None):
        fields['AddressID'] = cursor.lastrowid  
    print sql.insert(db, cursor, "{}Address".format(table), fields, keys_a) 
    
