# The libraries we'll need
import sys, cgi, redirect, session, html

# Get the session and check if logged in
sess = session.Session(expires=60*20, cookie_path='/')
loggedIn = sess.data.get('loggedIn')

# ---------------------------------------------------------------------------------------------------------------------
# send session cookie
print "%s\nContent-Type: text/html\n" % (sess.cookie)

# debug - what's in the session
#print(sess.data)
#sys.exit()

if loggedIn:
    
    # redirect to home page
    print html.do_redirect("home.py")
    
else:

    print html.make_head("login.css", title="WWAG Login")

    print html.make_navbar(loggedIn, 'N')

    print """
        <div id = "login_form">
            <h2> Sign In </h2>
            <fieldset>
            <form method="post" action="do_login.py">
                <p class="meta">Username <input type="text" name="username" /></p>
                <p class="meta">Password <input type="password" name="password" /></p>
                <input type="submit" id="search-submit" value="Login" onClick="DoSubmit()" />
            </form>
            </fieldset>
        </div>
    """

    
    # Footer at the end <p>The Footer</p>
    print html.end_html

# Tidy up and free resources
sess.close()
