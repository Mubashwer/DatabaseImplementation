# The libraries we'll need
import sys, cgi, session, redirect, MySQLdb, hashlib, uuid

# ---------------------------------------------------------------------------------------------------------------------
sess = session.Session(expires=20*60, cookie_path='/')
loggedIn = sess.data.get('loggedIn')

# ---------------------------------------------------------------------------------------------------------------------
# send session cookie
print "%s\nContent-Type: text/html\n" % (sess.cookie)

# ---------------------------------------------------------------------------------------------------------------------
# login logic
loggedIn = 0
if loggedIn:
    
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
    """ % redirect.getQualifiedURL("/~mskh/dbsys/mywork/home.py")
    
else:
    signedIn = False
    form = cgi.FieldStorage()
    if (form.has_key('username') and form.has_key('password')):
        
        db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003g29", "enigma29", "info20003g29", 3306)
        cursor = db.cursor()
        cursor.execute ("""
            SELECT UserName, Salt, HashedPassword
            FROM Player
            WHERE UserName = '{}'
        """.format (form["username"].value))
        
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
                WHERE UserName = '{}'
            """.format (form["username"].value))  

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

    whereToNext = "/~mskh/dbsys/mywork/greeting.py" 
    sess.close()
    
    #redirect to home page or back to the login page
    print """\
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <meta http-equiv="refresh" content="0;url=%s">
    </head>
    <body>
    </body>
    #""" % redirect.getQualifiedURL(whereToNext)

