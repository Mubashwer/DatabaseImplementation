# The libraries we'll need
import sys, cgi, redirect, session, MySQLdb, warnings

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
# Only logged in users who are players can access this page
if (0==1) and (not loggedIn or not userType == 'S'):
    # redirect to home page
    print """\
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <meta http-equiv="refresh" content="0;url=%s">
    </head>
    <body>
    </body>
    """ % redirect.getQualifiedURL("/~mskh/dbsys/dbs2014sm2group29/home.py")
    sess.close()   
    sys.exit(0)

# ---------------------------------------------------------------------------------------------------------------------
    
print """
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta name="keywords" content="" />
<meta name="description" content="" />
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<title>WWAG Instance Runs</title>
<link href="css/video_modify.css" rel="stylesheet" type="text/css" media="screen" />
</head>
<body>
"""

print """
<div class="main">
    <hi><a href="home.py">HOME</a></h1>
    <hi><a href="home.py">ABOUT US</a></h1>
</div>
"""

print """
<div class="search_form">
<h2 class="header">INSTANCE RUNS</h2>
<form action="instance_runs.py" method="post">
    <fieldset id="search">
        <legend>Maintain Instance Run</legend>
        
        <div class="textbox">
            <label for="InstanceRunID">Instance Run ID:</label>
            <input name="InstanceRunID" id="InstanceRunID" type="text" />
        </div>

        <div class="textbox">
            <label for="SupervisorID">Supervisor ID:</label>
            <input name="SupervisorID" id="SupervisorID" type="text" />
        </div>
        
         <div class="textbox">
            <label for="InstanceName">Instance Name:</label>
            <input name="InstanceName" id="InstanceName" type="text" />
        </div>
        
        <div class="textbox">
            <label for="RecordedTime">Recorded Time:</label>
            <input name = "RecordedTime" id= "RecordedTime" type="datetime-local" step=1>
        </div>

        <div class="textbox">
            <label for="CategoryName">Category Name:</label>
            <input name="CategoryName" id="CategoryName" type="text" />
        </div>

    </fieldset>
    
    <div id="buttons" class="button_select">
        <input type="reset" value="Reset" />
        <input type="submit" name="submit" value="Insert" />
        <input type="submit" name="submit" value="Search" />
    </div>
</form>
</div>
"""

####### CONNECT TO DATABASE AND LOAD FORM DATA ##########################################################################

db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003g29", "enigma29", "info20003g29", 3306)
cursor = db.cursor()
keys = ['InstanceRunID', 'SupervisorID', 'InstanceName', 'RecordedTime', 'CategoryName']
fields = dict.fromkeys(keys)

for key in fields:
    fields[key] = 'DEFAULT'        

for key in fields:
    if form.getvalue(key) != None:
        fields[key] = "'" + form.getvalue(key) + "'"        

######## If INSERT button is pressed then ... ###########################################################################
if form.getvalue("submit") == "Insert":

    #insert query is generated and there is an attempt to execute the query
    query = '''INSERT INTO InstanceRun VALUES ({}, {}, {}, {}, {});'''.format(fields[keys[0]], fields[keys[1]], fields[keys[2]], fields[keys[3]], fields[keys[4]])
    try:   
        cursor.execute(query)
        db.commit()
        print '<div class = "success">Insert Successful!</div>'
    except Exception, e:
        print '<div class = "error">Insert Error! {}.</div>'.format(repr(e))


######## If DELETE button is pressed then ... ###########################################################################        
if form.getvalue("submit") == "Delete":
    query = "DELETE FROM InstanceRun WHERE InstanceRunID = {};".format(fields[keys[0]])
    try:   
        cursor.execute(query)
        db.commit()
        print '<div class = "success">Delete Successful!</div>'
    except Exception, e:        
        print '<div class = "error">Delete Error! {}.</div>'.format(repr(e))
        
######## If UPDATE button is pressed then ... ############################################################################
if form.getvalue("submit") == "Update":        
    query = "UPDATE InstanceRun SET "
    for key in keys:
        query += "{} = {}, ".format(key, fields[key])
        
    query = query[:-2] + " WHERE InstanceRunID = {};".format(fields[keys[0]])
    
    try:   
        cursor.execute(query)
        db.commit()
        print '<div class = "success">Update Successful!</div>'
    except Exception, e:
        print query
        print '<div class = "error">Update Error! {}.</div>'.format(repr(e))       

####### GENERATE AND EXECUTE SEARCH QUERY  ################################################################################

query = "SELECT * FROM InstanceRun LIMIT 10;"
condition = "WHERE "
has_condition = False
                                                                                         
for key in fields:
    if fields[key] != 'DEFAULT':                                                                                     
        if key[-4:] == 'Name':
            condition += "{} LIKE '%{}%' AND ".format(key, form.getvalue(key))
        else:
            condition += "{} = {} AND ".format(key, fields[key])                                                                                           
        has_condition = True
                                                                                          
                                                                                         
if has_condition:
    query = query[:-9] + condition[:-4] + "LIMIT 10;"                                                                                                                                                                              

rows = None    
try:   
    cursor.execute(query)
    rows = cursor.fetchall()
except Exception, e:   
    print '<div class = "error">Search Error! {}.</div>'.format(repr(e))
    
####### DISPLAY RESULTS TABLE  #############################################################################################
print '<table>'

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
        print '<form action="instance_runs.py" method="post">'
        i = 0
        i += 1
        print '<td><input name="InstanceRunID" id="InstanceRunID" type="hidden" value = "{0}" />{0}</td>'.format(row[i])
        # Print each field of row as textbox
        for key in keys[1:]:
            if row[i] == None:
                field = ''
            else:
                field = row[i]
            print '<td><span class="row_textbox"><input name="{0}" id="{0}" type="text" value = "{1}" /></span></td>'.format(key, field)
            i += 1
        print '<td><input type="submit" name="submit" value="Update" /></td><td><input type="submit" name="submit" value="Delete" /></td>'
        print '</form>'
        print '</tr>'
                                                                                             
print '</table>'    
                                                                                         
print """
</body>
</html>
"""

# Tidy up and free resources
cursor.close()
db.close()
sess.close()                                                                                        

