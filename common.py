def make_head(title = 'WWAG', css_file = '', head_inject = ''):
    """Constructs and returns the html header. head_inject will be inserted directly after the 
    opening <head> tag.  It could, for example, contain a <meta> tag used to implement
    a redirect.  The string returned also initialises the <html> and <body> branches.
    All text following it's print-out will be part of the body."""
    
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
    """.format(head_inject, css_file, title)

def make_navbar():
    """Constructs and returns html string for the basic navbar used by most (all?) 
    pages on the site"""
    
    return  """
    <div id="header">
        <div id="navbar">
        <ul>
            <li><a href="login.py" style="text-decoration:none;color:#fff">Log In</a></li>
            <li><a href="aboutme.py" style="text-decoration:none;color:#fff">About Us</a></li>    
            <li><a href="videos_search.py" style="text-decoration:none;color:#fff">Videos</a></li>
            <li><a href="home.py" style="text-decoration:none;color:#fff">Home</a></li>
        </ul>
        </div>
    </div>
    """

def end_html():
    """Generates string of closing </body> and </html> tags to finish an html document."""
    
    return """
</body>
</html>
    """
