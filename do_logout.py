# The libraries we'll need
import sys, cgi, session, redirect, html

# ---------------------------------------------------------------------------------------------------------------------
sess = session.Session(expires=20*60, cookie_path='/')
alreadyLoggedOut = not sess.data.get('loggedIn')

if not alreadyLoggedOut:
    sess.data['loggedIn'] = 0 # log them out
    sess.data['userName'] = "None"
    sess.data['userType'] = 'N'
    sess.set_expires('') # expire session
    sess.close()

# ---------------------------------------------------------------------------------------------------------------------
# send session cookie
print "%s\nContent-Type: text/html\n" % (sess.cookie)

# ---------------------------------------------------------------------------------------------------------------------
# redirect to home page
print html.do_redirect("home.py")

