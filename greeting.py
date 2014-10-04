# The libraries we'll need
import sys, cgi, session, redirect, MySQLdb, time

# ---------------------------------------------------------------------------------------------------------------------
sess = session.Session(expires=20*60, cookie_path='/')
loggedIn = sess.data.get('loggedIn')

# ---------------------------------------------------------------------------------------------------------------------
# send session cookie
print "%s\nContent-Type: text/html\n" % (sess.cookie)

# ---------------------------------------------------------------------------------------------------------------------
# login logic

# ---------------------------------------------------------------------------------------------------------------------
# Send head of HTML document, pointing to our style sheet

print """
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta name="keywords" content="" />
<meta name="description" content="" />
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<title>Our Sample - Login page</title>
<link href="css/login.css" rel="stylesheet" type="text/css" media="screen" />
</head>
<body>
"""
if not loggedIn:
    status = "Unsuccessful"
    message = "The username or password you've entered doesn't match our records."
    whereToNext = "/~mskh/dbsys/mywork/login.py"
    div_id = "message_fail" 
    
elif sess.data.get('userType') == 'S' or sess.data.get('userType') == 'C':
    db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "mskh", "C1302762", "mskh", 3306)
    cursor = db.cursor()
    
    cursor.execute ("""
        SELECT FirstName, LastName
        FROM Player
        WHERE UserName = '{}'
    """.format (sess.data.get('userName')))
        
    if cursor.rowcount < 1:
        cursor.execute ("""
            SELECT FirstName, LastName
            FROM Viewer NATURAL JOIN CrowdFundingViewer
            WHERE UserName = '{}'
         """.format (sess.data.get('userName')))  

    div_id = "message"
    status = "Successful"
    row = cursor.fetchone();
    firstName = row[0];
    lastName = row[1];
    message = "Welcome back, " + firstName + " " + lastName + "!"
    whereToNext = "/~mskh/dbsys/mywork/home.py" 
    # tidy up
    cursor.close()
    db.close()

else:
    status = "Successful"
    message = "Welcome back!"                        
    div_id = "message"
    whereToNext = "/~mskh/dbsys/mywork/home.py"                     
    
    
print """
    <div id = "greeting">
        <h2> Login {} </h2>
        <div id = "{}">
            {}</br><span id=redirect>Redirecting in 5 seconds...</span>
        </div>
    </div>
""".format(status, div_id, message)
                        
# Tidy up and free resources
sess.close()                        

print """<meta http-equiv="refresh" content="5;url={}">""" .format(redirect.getQualifiedURL(whereToNext))                       

                        

    
# Footer at the end <p>The Footer</p>
print """
            
</body>
</html>
"""

