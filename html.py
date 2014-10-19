import Script, redirect, os

def make_head(css_file, title = 'WWAG', extra_script = ""):
    """Constructs and returns the html header"""
    
    return"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<title>{}</title>
<link href="css/{}" rel="stylesheet" type="text/css" media="screen" />
<script type="text/javascript">
{}
{}
</script>
</head>
<body>
    """.format(title, css_file, extra_script, Script.script)


def make_navbar(loggedIn, userType):
    """Constructs and returns html string for the basic navbar used by most (all?) 
    pages on the site"""
    href = {None: ('Log In', 'login.py'), 0: ('Log In', 'login.py'), 1: ('Log Out', 'do_logout.py')}

    if (not loggedIn or not userType == 'S'):
        return """
<div id="header">
        <div id="navbar">
        <ul>
            
            <li><a href="{}" style="text-decoration:none;color:#fff">{}</a></li>
            <li><a href="aboutme.py" style="text-decoration:none;color:#fff">About Us</a></li>
             <li><a href="venues.py" style="text-decoration:none;color:#fff">Venues</a></li>
            <li><a href="videos_search.py" style="text-decoration:none;color:#fff">Videos</a></li>
            <li><a href="home.py" style="text-decoration:none;color:#fff">Home</a></li>                  
        </ul>
        </div>
    </div>
    """.format(href[loggedIn][1], href[loggedIn][0])
    else:        
        return """
   <div id="header">
                <div id="navbar">
                    <ul>
                <li><a href="do_logout.py" style="text-decoration:none;color:#fff">Log Out</a></li>
                <li><a href="aboutme.py" style="text-decoration:none;color:#fff">About Us</a></li>
                <li><a href="players.py" style="text-decoration:none;color:#fff">Players</a></li>
                <li><a href="games.py" style="text-decoration:none;color:#fff">Games</a></li>
                <li><a href="instance_runs.py" style="text-decoration:none;color:#fff">Instance Runs</a></li>
                <li><a href="achievements.py" style="text-decoration:none;color:#fff">Achievements</a></li>
                <li><a href="viewers.py" style="text-decoration:none;color:#fff">Viewers</a></li>
                <li><a href="venues.py" style="text-decoration:none;color:#fff">Venues</a></li>
                <li><a href="videos_modify.py" style="text-decoration:none;color:#fff">Videos</a></li>
                <li><a href="home.py" style="text-decoration:none;color:#fff">Home</a></li>
                    </ul>
                </div>
      </div>
    """


def do_redirect(script, delay=0):
    """Constructs and returns the html header"""
    url = os.path.split(os.environ['REQUEST_URI'])[0] + '/' + script
    return"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<meta http-equiv="refresh" content="{};url={}">
</head>
<body>
    """.format(delay, redirect.getQualifiedURL(url))

end_html = """
</body>
</html>
    """

def wrap_p(text, p_id=None):
    if p_id:
        return '<p id="{}">'.format(p_id) + text + '</p>\n'
    else:
        return "<p>" + text + "</p>\n"

def wrap_div(text, div_id=None):
    return "<div id='{}'>".format(div_id) + text + "</div>"

def wrap_link(text, href=None):
    return "<a href='{}'>".format(href) + text + "</a>"

def wrap_tr(text):
    return "<tr>" + text + "</tr>\n"

def wrap_td(text):
    return "<td>" + text + "</td>"

def wrap_table(text):
    return "<table>\n" + text + "\n</table>\n"

def wrap_form(text, action = None):
    return "<form name='form' action='{}' method='post'>\n<fieldset>\n".format(action) \
+ text + "\n</fieldset>\n</form>\n "


