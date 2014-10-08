# The libraries we'll need
import sys, cgi, redirect, session

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
    
else:

    # ---------------------------------------------------------------------------------------------------------------------
    # Send head of HTML document, pointing to our style sheet
    print """
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta name="keywords" content="" />
    <meta name="description" content="" />
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <title>WWAG - Login</title>
    <link href="css/login.css" rel="stylesheet" type="text/css" media="screen" />
    </head>
    <body>
    """

    # Main HTML content, starting with header and main menu
    print """
    <div id="header">
		<div id="navbar">
			<ul>
            <li><a href="home.py" style="text-decoration:none;color:#fff">Home</a></li>
            <li><a href="Aboutme.py" style="text-decoration:none;color:#fff">About Us</a></li>
            <li><a href="logout.py" style="text-decoration:none;color:#fff">Log Out</a></li>
            <li><a href="video_search.py" style="text-decoration:none;color:#fff">Videos</a>
                <ul>
					<li><a href="#" style="text-decoration:none;color:#fff">Video 1</a></li>
					<li><a href="#" style="text-decoration:none;color:#fff">Video 2</a></li>
                    <li><a href="#" style="text-decoration:none;color:#fff">Video 3</a></li>
				</ul>
          </li>
              
			</ul>
		</div>
			
	</div>
    """

    print """
        <div id = "login_form">
            <h2> Sign In </h2>
            <fieldset>
            <form method="post" action="do_login.py">
                <p class="meta">Username <input type="text" name="username" /></p>
                <p class="meta">Password <input type="password" name="password" /></p>
                <input type="submit" id="search-submit" value="Login" />
            </form>
            </fieldset>
        </div>
    """

    
    # Footer at the end <p>The Footer</p>
    print """
            
    </body>
    </html>
    """

# Tidy up and free resources
sess.close()
​
