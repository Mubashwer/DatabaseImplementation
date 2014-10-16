def make_head(title = 'WWAG', css_file = None, head_inject = ''):
    """Constructs and returns the html header, taking as title and head_inject as inputs.
    title will be the window title.  head_inject will be inserted directly after the 
    opening <head> tag.  It could, for example, contain a <meta> tag used to implement
    a redirect.  The string returned also initialises the <html> and <body> branches.
    All text following will be part of the body."""
    
    return"""
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    {}
    <meta name="keywords" content="" />
    <meta name="description" content="" />
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <title>{}</title>
    <link href="css/{}" rel="stylesheet" type="text/css" media="screen" />
</head>
<body>
    """.format(head_inject, title, css_file)

def make_navbar():
    """Constructs and returns html string for the basic navbar used by most (all?) 
    pages on the site"""
    
    if (not loggedIn or not userType == 'N'):
   
    print """
    <div id="header">
        <div id="navbar">
        <ul>
            <li><a href="login.py" style="text-decoration:none;color:#fff">Log In</a></li>
            <li><a href="Aboutme.py" style="text-decoration:none;color:#fff">About Us</a></li>
        
            <li><a href="video_search.py" style="text-decoration:none;color:#fff">Videos</a></li>
            <li><a href="home.py" style="text-decoration:none;color:#fff">Home</a></li>
              
        </ul>
        </div>
        </div>
        """


    else:
    
    print """
    <div id="header">
        <div id="navbar">
            <ul>
            <li><a href="logout.py" style="text-decoration:none;color:#fff">Log Out</a></li>
            <li><a href="Aboutme.py" style="text-decoration:none;color:#fff">About Us</a></li>
            <li><a href="players.py" style="text-decoration:none;color:#fff">Players</a></li>
            <li><a href="games.py" style="text-decoration:none;color:#fff">Games</a></li>
            <li><a href="instance.py" style="text-decoration:none;color:#fff">Instance Runs</a></li>
            <li><a href="achievements.py" style="text-decoration:none;color:#fff">Achievements</a></li>
            <li><a href="Viewers.py" style="text-decoration:none;color:#fff">Viewers</a></li>
            <li><a href="video_search.py" style="text-decoration:none;color:#fff">Videos</a></li>
            <li><a href="home.py" style="text-decoration:none;color:#fff">Home</a></li>
            </ul>
        </div>
    </div>
"""

end_html = """
</body>
</html>
    """
def results_as_dicts(cursor):
    """
    Takes a MySQLdb cursor object and returns a list of dictionaries, each representing a row
    returned by the most recent query, with attribute names as keys and values as values
    """
    headings = [tup[0] for tup in cursor.description]
    rows = cursor.fetchall()
    dict_rows = [dict(zip(headings, row)) for row in rows]
    return dict_rows​​
    
def uniq(l):
    return sorted(list(set(l)))#Cast to set, then back to remove dups

def wrap_p(text, p_id=None):
    if p_id:
        return "<p id='{}'>".format(p_id) + text + "</p>\n"
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
+ text + "\n</fieldset>\n</form>\n"
​
