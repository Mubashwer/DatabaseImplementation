# The libraries we'll need
import sys, cgi, session, redirect, MySQLdb, hashlib, uuid, html

# ---------------------------------------------------------------------------------------------------------------------
sess = session.Session(expires=20*60, cookie_path='/')
loggedIn = sess.data.get('loggedIn')

# ---------------------------------------------------------------------------------------------------------------------
# send session cookie
print "%s\nContent-Type: text/html\n" % (sess.cookie)

# ---------------------------------------------------------------------------------------------------------------------
# login logic

if loggedIn:
    
    # redirect to home page
    print html.do_redirect("home.py")
    
else:
    signedIn = False
    form = cgi.FieldStorage()
    if (form.has_key('username') and form.has_key('password')):
        
        db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003g29", "enigma29", "info20003g29", 3306)
        cursor = db.cursor()
        cursor.execute ("""
            SELECT UserName, Salt, HashedPassword
            FROM Player
            WHERE UserName = %s ;
        """, (form["username"].value, ))
        
        if cursor.rowcount == 1:
            row = cursor.fetchone()
            salt = row[1]
            actual_password = row[2]
            given_password = hashlib.sha512(form["password"].value + salt).hexdigest()
             
            if actual_password == given_password:
                 signedIn = True
                 userType = 'S'
        
        else:
            cursor.execute ("""
                SELECT UserName, Salt, HashedPassword, ViewerType
                FROM Viewer
                WHERE UserName = %s ;
            """, (form["username"].value, ))  

            if cursor.rowcount == 1:
                row = cursor.fetchone()
                salt = row[1]
                actual_password = row[2]
                given_password = hashlib.sha512(form["password"].value + salt).hexdigest()
                if actual_password == given_password:
                     signedIn = True        
                     userType = row[3]
        
             
        if(signedIn == True):
            sess.data['loggedIn'] = 1
            sess.data['userName'] = form["username"].value
            sess.data['userType'] = userType
        else:
            sess.data['loggedIn'] = 0
        

        # tidy up
        cursor.close()
        db.close()
    sess.close()
    
    #redirect to greeting page
    print html.do_redirect("greeting.py")
