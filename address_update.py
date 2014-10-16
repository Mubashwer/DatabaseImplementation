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
    
print html.make_head("video_modify.css", title="WWAG Address")

print html.make_navbar(loggedIn, userType)

# ---------------------------------------------------------------------------------------------------------------------
####### CONNECT TO DATABASE LOAD ADDRESS DATA ##########################################################################

db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003g29", "enigma29", "info20003g29", 3306)
cursor = db.cursor()
table = 'Address'
keys = ['AddressID', 'StreetNumber', 'StreetNumberSuffix', 'StreetName', 'StreetType', 'AddressType', 'AddressTypeIdentifier', 'MinorMunicipality', 'MajorMunicipality', 'GoverningDistrict', 'PostalArea', 'Country']
ignore = ['StreetNumber', 'StreetNumberSuffix', 'StreetName', 'StreetType', 'AddressType', 'AddressTypeIdentifier', 'MinorMunicipality', 'MajorMunicipality', 'GoverningDistrict', 'PostalArea', 'Country']
pk = ['AddressID']
fields = dict.fromkeys(keys)


for key in fields:
    fields[key] = form.getvalue(key)
message = ""

######## If UPDATE button is pressed then ... ############################################################################
if form.getvalue("submit") == "Update":        
    message =  sql.update(db, cursor, table, fields, keys, pk)

        
####### GENERATE AND EXECUTE SEARCH QUERY ##########################################################################
result =  sql.search(db, cursor, table, fields, keys, pk, ignore=ignore, limit=10, fetch_one=True)
row = result[0];


if row == None:
    row = ["", "", "", "", "", "",  "", "", "", "", "", ""]

row = list(row)
for i in range(12):
    if row[i] == None:
        row[i] = ""
    else:
        row[i] = escape(str(row[i]), entities)  

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
