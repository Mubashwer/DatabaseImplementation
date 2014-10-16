# The libraries we'll need
import sys, cgi, session, redirect, MySQLdb, time, html
from xml.sax.saxutils import *
entities = {'"': '&quot;'} 
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

print html.make_head("login.css", title="WWAG Greeting")

if not loggedIn:
    status = "Unsuccessful"
    message = "The username or password you've entered doesn't match our records."
    whereToNext = "/~mskh/dbsys/dbs2014sm2group29/login.py"
    div_id = "message_fail" 
    
elif sess.data.get('userType') == 'S' or sess.data.get('userType') == 'C':
    db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003g29", "enigma29", "info20003g29", 3306)
    cursor = db.cursor()
    
    cursor.execute ("""
        SELECT FirstName, LastName
        FROM Player
        WHERE UserName = %s ;
    """,(sess.data.get('userName'),))
        
    if cursor.rowcount < 1:
        cursor.execute ("""
            SELECT FirstName, LastName
            FROM Viewer NATURAL JOIN CrowdFundingViewer
            WHERE UserName = %s ;
         """, (sess.data.get('userName'),))  

    div_id = "message"
    status = "Successful"
    row = cursor.fetchone();
    firstName = escape(row[0], entities);
    lastName = escape(row[1], entities);
    message = "Welcome back, " + firstName + " " + lastName + "!"
    whereToNext = "/~mskh/dbsys/dbs2014sm2group29/home.py" 
    # tidy up
    cursor.close()
    db.close()

else:
    status = "Successful"
    message = "Welcome back!"                        
    div_id = "message"
    whereToNext = "/~mskh/dbsys/dbs2014sm2group29/home.py"                     
    
    
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
print html.end_html
