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
    if(document.forms.myForm.ViewerType[0].checked==true)
        show("crowd");
    else if(document.forms.myForm.ViewerType[1].checked==true)
        show("premium");
    else if(document.forms.myForm.ViewerType[2].checked==true) {
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
a_keys = ['AddressID', 'StreetNumber', 'StreetNumberSuffix', 'StreetName', 'StreetType', 'AddressType', 'AddressTypeIdentifier', 'MinorMunicipality', 'MajorMunicipality', 'GoverningDistrict', 'PostalArea', 'Country']
address_keys = ['ViewerID', 'AddressID', 'StartDate', 'EndDate']
address_exact = ['ViewerID', 'AddressID']
address_pk = ['ViewerID', 'AddressID', 'StartDate']
message = ""

fields = dict.fromkeys(keys + keys_c + keys_p + address_keys + ['ViewerTypeOld', 'StartDateOld'])

for key in fields:
    fields[key] = form.getvalue(key)

######## If UPDATE button is pressed then ... ############################################################################
ignore_update = [];
message2 = ""
if form.getvalue("submit") == "Update":        
    fields['Salt'] = uuid.uuid4().hex
    if fields["HashedPassword"] != None:
        fields["HashedPassword"] = hashlib.sha512(fields['HashedPassword'] + fields['Salt']).hexdigest()
    else:
        ignore_update = ['HashedPassword', 'Salt']
    

    error = 0    
    if(fields['ViewerType'] != fields['ViewerTypeOld']): #insert more tables if applicable if viewer type is changed
        if(fields['ViewerType'] == 'B' or fields['ViewerType'] == 'C'):
            if(fields['ViewerTypeOld'] == 'N' or fields['ViewerTypeOld'] == 'P'):
                message =  sql.insert(db, cursor, 'CrowdFundingViewer', fields, keys_c)
                print "insert"
                if 'Error' in message:
                    print message
                    error = 1
        if(fields['ViewerType'] == 'B' or fields['ViewerType'] == 'P'):
            if(fields['ViewerTypeOld'] == 'N' or fields['ViewerTypeOld'] == 'C'):
                message =  sql.insert(db, cursor, 'PremiumViewer', fields, keys_p)
                print "insert"
                if 'Error' in message:
                    print message
                    error = 1                
                
        if error == 1: #delete tables if there are any error
            if(fields['ViewerTypeOld'] == 'N' or fields['ViewerTypeOld'] == 'P'):
                sql.delete(db, cursor, 'CrowdFundingViewer', fields, ['ViewerID'])
            if(fields['ViewerTypeOld'] == 'N' or fields['ViewerTypeOld'] == 'C'):
                sql.delete(db, cursor, 'PremiumViewer', fields, ['ViewerID'])
            message2 = "Update Error! Error in changing types!"
        
        #delete tables if viewer is now no longer premium or crowdfunding
        if(fields['ViewerType'] == 'N' or fields['ViewerType'] == 'P'):
            sql.delete(db, cursor, 'CrowdFundingViewer', fields, ['ViewerID'])
        if(fields['ViewerType'] == 'N' or fields['ViewerType'] == 'C'):
            sql.delete(db, cursor, 'PremiumViewer', fields, ['ViewerID'])
    

    #update current tables
    message =  sql.update(db, cursor, table, fields, keys, ['ViewerID'], ignore=ignore_update)
    if fields['ViewerTypeOld'] != 'C' or fields['ViewerTypeOld'] != 'B':
        message =  sql.update(db, cursor, 'CrowdFundingViewer', fields, keys_c, ['ViewerID'], ignore=ignore_update) 
    if fields['ViewerTypeOld'] != 'P' or fields['ViewerTypeOld'] != 'B':
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

check = {"C":0, "P":1, "B":2,"N":3}
types = ["", "", "", ""]
if(row[1] != ""):
    types[check[row[1]]] = 'checked="checked"'


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
            <label for="UserName">UserName:</label>
            <input name="UserName" id="UserName" type="text" value="{}"/>
        </div>

        <div class="textbox">
            <label for="HashedPassword">New Password:</label>
            <input name="HashedPassword" id="HashedPassword" type="text" />
        </div>

        <div class="textbox">
            <label for="ViewerType">Viewer Type:</label>
            <input type ="hidden" name="ViewerTypeOld" value="{}">
            <input type="radio" name="ViewerType"  value="C" {} onclick="details();">Crowdfunding<br />
            <input type="radio" name="ViewerType"  value="P" {} onclick="details();">Premium<br />
            <input type="radio" name="ViewerType"  value="B" {} onclick="details();">Both<br />
            <input type="radio" name="ViewerType"  value="N" {} onClick="details()">Regular

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
""".format(row[0], row[0], row[2], row[3], row[4], row[1], types[0], types[1], types[2], types[3] , row_c[1], row_c[2], row_c[3], row_p[1], row_p[1])
       
######## If CHANGE ADDRESS (Date, ID) button is pressed then ... ###########################################################################        
if form.getvalue("submit") == "Change":
    query = "UPDATE ViewerAddress SET StartDate = %s, EndDate = %s WHERE ViewerID = %s AND AddressID = %s AND StartDate = %s;"
    args = (fields['StartDate'], fields['EndDate'], fields['ViewerID'], fields['AddressID'], fields['StartDateOld'])

    try:   
        cursor.execute(query, args)
        db.commit()
        print '<div class = "success">Update Successful!</div>'
    except Exception, e:
        print '<div class = "error">Update Error! {}.</div>'.format(repr(e))
        
######## If DELETE ADDRESS button is pressed then ... ###########################################################################        
if form.getvalue("submit") == "DeleteAddress":
    print sql.delete(db, cursor, "ViewerAddress", fields, address_pk)
    print sql.delete(db, cursor, "Address", fields, ['AddressID'])
    
####### GENERATE AND EXECUTE SEARCH QUERY FOR ADDRESS  ################################################################################

result =  sql.search(db, cursor, "ViewerAddress", fields, address_keys, address_exact, select=["AddressID", "StartDate", "EndDate"], ignore=['AddressID', 'StartDate', 'EndDate'], order="ORDER BY StartDate DESC")
rows = result[0];
print result[1];

    
####### DISPLAY RESULTS TABLE  #############################################################################################
print message
print message2
                                        
print '''<div class="insert_button"><input type="button" onClick="parent.location='address_insert.py?ViewerID={}'" value='InsertAddress'></div>'''.format(form.getvalue(keys[0]))
print '<table class="gridtable" align="center">'

# Print column headers    
print '<tr>'
print "<th>AddressID</th><th>StartDate</th><th>EndDate</th><th>Change</th><th>Update</th><th>Delete</th>"
print '</tr>'

# Print each row of table    
if rows != None: 
    for row in rows:
        print '<tr>'
        print '<form action="viewer.py" method="get">'
        print '<input name="ViewerID" id="ViewerID" type="hidden" value ="{0}" />'.format(fields['ViewerID'])
        print '<td><input name="AddressID" id="AddressID" type="hidden" value ="{0}" />{0}</td>'.format(row[0])
        print '<td><input name="StartDateOld" id="StartDateOld" type="hidden" value ="{0}" /><input name="StartDate" id="StartDate" type="text" value ="{0}" /></td>'.format(escape(str(row[1]), entities))
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

