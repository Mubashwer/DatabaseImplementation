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
if 0 == 1 and (not loggedIn or not userType == 'S'):
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
<title>WWAG Players</title>
<link href="css/user_details.css" rel="stylesheet" type="text/css" media="screen" />
</head>
<body>
"""

print """
<div class="main">
    <hi><a href="home.py">HOME</a></h1>
    <hi><a href="home.py">ABOUT US</a></h1>
</div>
"""
 
####### LOAD FORM DATA ##########################################################################

db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003g29", "enigma29", "info20003g29", 3306)
cursor = db.cursor()
keys = ['GameID', 'Genre', 'Review', 'StarRating', 'ClassificationRating', 'PlatformNotes', 'PromotionLink', 'Cost', 'GameName']
fields = dict.fromkeys(keys)
row = None

for key in fields:
    fields[key] = 'DEFAULT'        

for key in fields:
    if form.getvalue(key) != None:
        fields[key] = "'" + form.getvalue(key) + "'"
        
        
######## If INSERT button is pressed then ... ###########################################################################
if form.getvalue("submit") == "Insert":

    #insert query is generated and there is an attempt to execute the query
    query = '''INSERT INTO Game VALUES ('''
    
    for key in keys:
        query += "{}, ".format(fields[key])
    
    query = query[:-2] + ");"

    try:   
        cursor.execute(query)
        db.commit()
        print '<div class = "success">Insert Successful!</div>'
    except Exception, e:
        print '<div class = "error">Insert Error! {}.</div>'.format(repr(e)) 

######## If UPDATE button is pressed then ... ############################################################################
if form.getvalue("submit") == "Update":        
    query = "UPDATE Game SET "
    for key in keys:
        query += "{} = {}, ".format(key, fields[key])
        
    query = query[:-2] + " WHERE GameID = {};".format(fields[keys[0]])
    
    try:   
        cursor.execute(query)
        db.commit()
        print '<div class = "success">Update Successful!</div>'
    except Exception, e:
        print '<div class = "error">Update Error! {}.</div>'.format(repr(e))  
        
######## LOAD RESULT ... ############################################################################
        
if fields['GameID'] != 'DEFAULT':
    
    query = "SELECT * FROM Game WHERE GameID = {}".format(fields['GameID'])    
    try:   
        cursor.execute(query)
        row = cursor.fetchone()
    except Exception, e:   
        print '<div class = "error">Search Error! {}.</div>'.format(repr(e))

if row == None:
    row = ["", "", "", "", "", "", "", "", ""]

row = list(row)
for i in range(9):
    if row[i] == None:
        row[i] = ""
        
######## If DELETE button is pressed then ... ###########################################################################        
if form.getvalue("submit") == "Delete":
    query = "DELETE FROM Game WHERE GameID = {};".format(fields[keys[0]])
    try:   
        cursor.execute(query)
        db.commit()
        print '<div class = "success">Delete Successful!</div>'
    except Exception, e:        
        print '<div class = "error">Delete Error! {}.</div>'.format(repr(e))

####### PRINT FORM ##############################################################################
        
print """
<div class="search_form">
<h2 class="header">GAMES</h2>
<form action="games.py" method="post">
    <fieldset id="search">
        <legend>Maintain Games</legend>
        
        <div class="textbox">
            <label for="GameID">Game ID:</label>
            <input name="GameID" id="GameID" type="text" value = "{0}" />
        </div>

        <div class="textbox">
            <label for="GameName">Game Name:</label>
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
        <input type="submit" name="submit" value="Insert" />
        <input type="submit" name="submit" value="Search" />
        <input type="submit" name="submit" value="Update" />
        <input type="submit" name="submit" value="Delete" />
    </div>
</form>
</div>
""".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]) 
 

####### GENERATE AND EXECUTE SEARCH QUERY  ################################################################################

query = "SELECT GameID, GameName FROM Game LIMIT 10;"
condition = "WHERE "
has_condition = False
                                                                                         
for key in fields:
    if fields[key] != 'DEFAULT':
        if key in ['GameID', 'StarRating', 'Cost']:
            condition += "{} = {} AND ".format(key, fields[key])         
        else:
            condition += "{} LIKE '%{}%' AND ".format(key, form.getvalue(key))                                                                                          
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
print '<th>GameID</th><th>GameName</th>'
print '</tr>'

# Print each row of table    
if rows != None: 
    for a_row in rows:
        print '<tr>'
        print '<td><a href="games.py?GameID={0}">{0}</a></td><td><a href="games.py?GameID={0}">{1}</a></td>'.format(a_row[0], a_row[1])
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
