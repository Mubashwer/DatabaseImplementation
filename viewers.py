
# The libraries we'll need
import sys, cgi, redirect, session, MySQLdb, warnings, hashlib, uuid, html, sql
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

js="""
function show(ladiv){
    document.getElementById(ladiv).style.display="inline";
}

function hide(ladiv){
    document.getElementById(ladiv).style.display="none";
}

function details(){
    hide("crowd");
    hide("premium");
    if(document.forms.myForm.ViewerType.value == 'C')
        show("crowd");
    else if(document.forms.myForm.ViewerType.value == 'P')
        show("premium");
    else if(document.forms.myForm.ViewerType.value == 'B') {
        show("crowd");
        show("premium");
    }    

}
"""
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

####### CONNECT TO DATABASE AND LOAD FORM DATA ##########################################################################

db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003g29", "enigma29", "info20003g29", 3306)
cursor = db.cursor()
table = 'Viewer'
keys = ['ViewerID', 'ViewerType', 'DateOfBirth','Email', 'UserName', 'HashedPassword', 'Salt']
keys_c = ['ViewerID', 'FirstName', 'LastName', 'TotalAmountDonated']
keys_p = ['ViewerID', 'RenewalDate']
exact_keys = ['ViewerID', 'TotalAmountDonated']
ignore_keys = ['ViewerType', 'DateOfBirth','Email', 'UserName', 'HashedPassword', 'Salt', 'FirstName', 'LastName', 'TotalAmountDonated', 'RenewalDate']
message = ""

fields = dict.fromkeys(keys + keys_c + keys_p + ['ViewerTypeOld'])

for key in fields:
    fields[key] = form.getvalue(key)

######## If UPDATE button is pressed then ... ############################################################################
ignore_update = [];
if form.getvalue("submit") == "Update":        
    fields['Salt'] = uuid.uuid4().hex
    if fields["HashedPassword"] != None:
        fields["HashedPassword"] = hashlib.sha512(fields['HashedPassword'] + fields['Salt']).hexdigest()
    else:
        ignore_update = ['HashedPassword', 'Salt']
    

    message =  sql.update(db, cursor, table, fields, keys, ['ViewerID'], ignore=ignore_update)
    if fields['ViewerType'] != 'C' or fields['ViewerType'] != 'B':
        message =  sql.update(db, cursor, 'CrowdFundingViewer', fields, keys_c, ['ViewerID'], ignore=ignore_update) 
    if fields['ViewerType'] != 'P' or fields['ViewerType'] != 'B':
        message =  sql.update(db, cursor, 'PremiumViewer', fields, keys_p, ['ViewerID'], ignore=ignore_update)          

                         
        
######## If DELETE button is pressed then ... ###########################################################################        
if form.getvalue("submit") == "Delete":
    message = sql.delete(db, cursor, table, fields, ['ViewerID'])
    
        
####### GENERATE AND EXECUTE SEARCH QUERY ##########################################################################

# Search Viewer from Viewers using ViewerID and ignoring other fields    
result =  sql.search(db, cursor, table, fields, keys, exact_keys, ignore=ignore_keys, limit=10, fetch_one=True)
row = result[0];

# If Viewer is found then check whether he/she is premium and/or crowdfunding and then search those table
row_c = ["", "", "", ""]
row_p = ["", ""]

if row == None:
    row = ["", "", "", "", "", "",  ""]
    
else:
    if(row[1] == 'B' or row[1] == 'C'):
        result =  sql.search(db, cursor, "CrowdFundingViewer", fields, keys_c, exact_keys, ignore=ignore_keys, limit=10, fetch_one=True)
        row_c = result[0];
        
        if row_c == None:
            row_c = ["", "", "", ""]

    
    if(row[1] == 'B' or row[1] == 'P'):
        result =  sql.search(db, cursor, "PremiumViewer", fields, keys_p, exact_keys, ignore=ignore_keys, limit=10, fetch_one=True)
        row_p = result[0];

        if row_p == None:
            row_p = ["", ""]

        
row = list(row)
for i in range(7):
    if row[i] == None:
        row[i] = ""
    else:
        row[i] = escape(str(row[i]), entities)
        
row_c = list(row_c)
for i in range(4):
    if row_c[i] == None:
        row_c[i] = ""
    else:
        row_c[i] = escape(str(row_c[i]), entities) 
        
row_p = list(row_p)
for i in range(2):
    if row_p[i] == None:
        row_p[i] = ""
    else:
        row_p[i] = escape(str(row_p[i]), entities)



    

####### PRINT FORM ##############################################################################
    
print html.make_head("video_modify.css", title="WWAG Viewers", extra_script=js)

print html.make_navbar(loggedIn, userType)


print """
<div class="search_form">
<h2 class="header">VIEWERS</h2>
<form name ="myForm" id="myForm" action="viewer.py" method="get">
    <fieldset id="search">
        <legend>Maintain Viewer</legend>
        
        <div class="textbox">
            <label for="ViewerID">Viewer ID:</label>
            <input name="ViewerID" id="ViewerID" type="hidden" value="{}"/>
            <span class = "just_text">{}</span>
        </div>
        
         <div class="textbox">
            <label for="DateOfBirth">Date of Birth:</label>
            <input name="DateOfBirth" id="DateOfBirth" type="date" value="{}"/>
        </div>
        
        <div class="textbox">
            <label for="Email">Email:</label>
            <input name = "Email" id= "Email" type="text" value="{}"/>
        </div>
        
        <div class="textbox">
            <label for="Player Type">UserName:</label>
            <input name="UserName" id="UserName" type="text" value="{}"/>
        </div>

        <div class="textbox">
            <label for="HashedPassword">New Password:</label>
            <input name="HashedPassword" id="HashedPassword" type="text" />
        </div>

        <div class="textbox">
            <label for="ViewerType">Viewer Type:</label>
            <input type="radio" name="ViewerType"  value="{}" checked="checked" onclick="details();">{}<br />

        </div>
        
        <div id = "crowd"><div class="textbox">
            <label for="FirstName">First Name:</label>
            <input name="FirstName" id="FirstName" type="text" value="{}"/>
        </div>

        <div class="textbox">
            <label for="LastName">Last Name:</label>
            <input name="LastName" id="LastName" type="text" value="{}"/>
        </div>

        <div class="textbox">
            <label for="TotalAmountDonated">Total Amount Donated:</label>
            <input name="TotalAmountDonated" id="TotalAmountDonated" type="text" value="{}"/>
        </div></div>

        <div id = "premium"><div class="textbox">
            <label for="RenewalDate">RenewalDate:</label>
            <input name="RenewalDate" id="RenewalDate" type="date" value="{}" />
        </div></div>


    </fieldset>
    
    <div id="buttons" class="button_select">
        <input type="reset" value="Reset" />
        <input type="submit" name="submit" value="Update" />
        <input type="submit" name="submit" value="Delete" />
    </div>
</form>
</div>
<script type="text/javascript">
details();
</script>
""".format(row[0], row[0], row[2], row[3], row[4], row[1], row[1] , row_c[1], row_c[2], row_c[3], row_p[1], row_p[1])
       

    
print message                                                                                         
print html.end_html
                     
# Tidy up and free resources
cursor.close()
db.close()
sess.close()  
