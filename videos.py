# The libraries we'll need
import sys, cgi, redirect, session

# Get the session and check if logged in
sess = session.Session(expires=60*20, cookie_path='/')
loggedIn = sess.data.get('loggedIn')

# ---------------------------------------------------------------------------------------------------------------------
# send session cookie
print "%s\nContent-Type: text/html\n" % (sess.cookie)

print """
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta name="keywords" content="" />
<meta name="description" content="" />
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<title>WWAG Videos</title>
<link href="css/login.css" rel="stylesheet" type="text/css" media="screen" />
</head>
<body>
"""
print """
<div class="search_form">
<h2 class="header">VIDEOS</h2>
<form action="{}" method="post">
    <fieldset id="search">
        <legend>Video Search</legend>
        

        <div class="textbox">
            <label for="video_id">Video ID:</label>
            <input name="video_id" id="video_id" type="text" />
        </div>
        
         <div class="textbox">
            <label for="game_id">Game ID:</label>
            <input name="game_id" id="game_id" type="text" />
        </div>

        <div class="textbox">
            <label for="game_name">Game Name:</label>
            <input name="game_name" id="game_name" type="text" />
        </div>

        <div class="textbox">
            <label for="instance_run_id">InstanceRun ID:</label>
            <input name="instance_run_id" id="instance_run_id" type="text" />
        </div>

        <div class="textbox">
            <label for="instance_run_name">InstanceRun Name:</label>
            <input name="instance_run_name" id="instance_run_name" type="text" />
        </div>

         <div class="textbox">
            <label for="price">Price:</label>
            <input name="price" id="price" type="text" />
        </div>
        
        <div class="radio">
            <input type="radio" name="video_type" id="premium" value="P"><span>Premium</span>    
            <input type="radio" name="video_type" id="crowdfunding" value="C"><span>CrowdFunding</span>
        </div>
    
    </fieldset>
    <div id="buttons" class="button_select">
        <input type="reset" value="Reset" />
        <input type="submit" value="Submit" />
    </div>
</form>
</div>
"""

print """
</body>
</html>
"""

# Tidy up and free resources
sess.close()​​​
