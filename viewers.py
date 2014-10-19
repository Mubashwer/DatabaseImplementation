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

# ---------------------------------------------------------------------------------------------------------------------
    
print html.make_head("video_modify.css", title="WWAG Viewers", extra_script=js)

print html.make_navbar(loggedIn, userType)


print """
<div class="search_form">
<h2 class="header">VIEWERS</h2>
<form name ="myForm" id="myForm" action="viewers.py" method="get">
    <fieldset id="search">
        <legend>Maintain Viewer</legend>
        
        <div class="textbox">
            <label for="ViewerID">Viewer ID:</label>
            <input name="ViewerID" id="ViewerID" type="text" />
        </div>
        
         <div class="textbox">
            <label for="DateOfBirth">Date of Birth:</label>
            <input name="DateOfBirth" id="DateOfBirth" type="date" />
        </div>
        
        <div class="textbox">
            <label for="Email">Email:</label>
            <input name = "Email" id= "Email" type="text" />
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
            <label for="ViewerType">Viewer Type:</label>
            <input type="radio" name="ViewerType"  value="C" onclick="details();">Crowdfunding<br />
            <input type="radio" name="ViewerType"  value="P" onclick="details();">Premium<br />
            <input type="radio" name="ViewerType"  value="B" onclick="details();">Both<br />
            <input type="radio" name="ViewerType"  value="N" checked="checked" onClick="details()">Regular
        </div>
        
        <div id = "crowd"><div class="textbox">
            <label for="FirstName">First Name:</label>
            <input name="FirstName" id="FirstName" type="text" />
        </div>

        <div class="textbox">
            <label for="LastName">Last Name:</label>
            <input name="LastName" id="LastName" type="text" />
        </div>

        <div class="textbox">
            <label for="TotalAmountDonated">Total Amount Donated:</label>
            <input name="TotalAmountDonated" id="TotalAmountDonated" type="text" />
        </div></div>

        <div id = "premium"><div class="textbox">
            <label for="RenewalDate">RenewalDate:</label>
            <input name="RenewalDate" id="RenewalDate" type="date" />
        </div></div>


    </fieldset>
    
    <div id="buttons" class="button_select">
        <input type="reset" value="Reset" />
        <input type="submit" name="submit" value="Insert" />
        <input type="submit" name="submit" value="Search" onClick="DoSubmit()" />
    </div>
</form>
</div>
<script type="text/javascript">
details();
</script>
"""

####### CONNECT TO DATABASE AND LOAD FORM DATA ##########################################################################

db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003g29", "enigma29", "info20003g29", 3306)
cursor = db.cursor()
table = 'Viewer'
keys = ['ViewerID', 'ViewerType', 'DateOfBirth','Email', 'UserName', 'HashedPassword', 'Salt']
ignore_keys = ['ViewerType', 'DateOfBirth','Email', 'UserName', 'HashedPassword', 'Salt']
keys_c = ['ViewerID', 'FirstName', 'LastName', 'TotalAmountDonated']
keys_p = ['ViewerID', 'RenewalDate']
exact_keys = ['ViewerID', 'TotalAmountDonated']
ignore = ['HashedPassword', 'Salt']

fields = dict.fromkeys(keys + keys_c + keys_p)

for key in fields:
    fields[key] = form.getvalue(key)       

######## If INSERT button is pressed then ... ###########################################################################
message = ""
stop = 0
if form.getvalue("submit") == "Insert":
    fields['Salt'] = uuid.uuid4().hex
    if fields["HashedPassword"] != None:
        fields["HashedPassword"] = hashlib.sha512(fields['HashedPassword'] + fields['Salt']).hexdigest()
    else:
        print '<div class = "error">Insert Error! Password is empty.</div>'
        sys.exit(0);
        print html.end_html      
    
    # Insert into main viewers table
    message =  sql.insert(db, cursor, table, fields, keys)
    if 'Error!' in message:
        stop = 1
    
    if(fields['ViewerID'] == None):
        fields['ViewerID'] = cursor.lastrowid        
    
    #Insert into subtypes if applicable and delete viewer if there is any error in inserting in subtypes table
    if stop == 0 and (fields['ViewerType'] == 'B' or fields['ViewerType'] == 'C'):
          message =  sql.insert(db, cursor, 'CrowdFundingViewer', fields, keys_c)
          if 'Error!' in message:
            sql.delete(db, cursor, table, fields, ['ViewerID'])
            stop = 1

        
    if stop == 0 and (fields['ViewerType'] == 'B' or fields['ViewerType'] == 'P'):
          message =  sql.insert(db, cursor, 'PremiumViewer', fields, keys_p)              
          if 'Error!' in message:
              sql.delete(db, cursor, table, fields, ['ViewerID'])

    
print message                                                                                         
print html.end_html

####### GENERATE AND EXECUTE SEARCH QUERY  ################################################################################

result =  sql.search(db, cursor, table, fields, keys, exact_keys, select=["ViewerID", "UserName"], ignore=ignore_keys, limit=10)

rows = result[0];
print result[1]; 
    
####### DISPLAY RESULTS TABLE  #############################################################################################
print '<table class="gridtable" align="center">'

# Print column headers    
print '<tr>'
print '<th>ViewerID</th><th>UserName</th>'
print '</tr>'

# Print each row of table    
if rows != None: 
    for row in rows:
        print '<tr>'
        print '<td><a href="viewer.py?ViewerID={0}">{0}</a></td><td><a href="viewer.py?ViewerID={0}">{1}</a></td>'.format(escape(str(row[0])), escape(str(row[1])))
        print '</tr>'
                                                                                             
print '</table>'    
                                                                                         
print html.end_html
                     
# Tidy up and free resources
cursor.close()
db.close()
sess.close()    

