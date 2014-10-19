# The libraries we'll need
import sys, cgi, redirect, session, MySQLdb, html, warnings
from xml.sax.saxutils import *

warnings.filterwarnings('error', category=MySQLdb.Warning)

# Get the session and check if logged in
sess = session.Session(expires=60*20, cookie_path='/')
loggedIn = sess.data.get('loggedIn')
userType = sess.data.get('userType')

form = cgi.FieldStorage()
db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003g29", "enigma29", "info20003g29", 3306)
# ---------------------------------------------------------------------------------------------------------------------
mnm = form.getvalue("mnm")
#ModelAndMake: mnm
query = "SELECT * FROM Equipment WHERE ModelAndMake='{}'".format(mnm)
try:
    db.query(query)
    res = db.store_result()
    rows = res.fetch_row(maxrows = 0, how = 1)
    assert(len(rows) > 0)
    query_success = True
except AssertionError, e:
    query_success = False
    message = """
    <p id='select_error' class='error'>
    No results were returned for the given model and make.
    </p>
    """
except Exception, e:
    query_success = False
    message = """
    <p id='select_error' class='error'>
    Database error : {}
    </p>
    """.format(repr(e))

if not query_success:
    body = message
else:
    body = """
    <table>
        <tr id='mnm'>
            <td>Model and make:</td>
            <td>{}</td>
        </tr>
        <tr id='pspeed'>
            <td>Processor speed:</td>
            <td>{}</td>
        </tr>
        <tr id='reviewlabel'>
            <td colspan='2'>Review(s):</td>
        </tr>
    """.format(escape(str(rows[0]["ModelAndMake"])), escape(str(rows[0]["ProcessorSpeed"])))
    
    for result in rows:
        body += """
        <tr class = 'review'>
            <td colspan='2'>{}</td>
        </tr>
         """.format(escape(str(result["EquipmentReview"])))
    body += """
    </table>
    """
    
# send session cookie
print "%s\nContent-Type: text/html\n" % (sess.cookie)

if not mnm:
    mnm = "None"

print html.make_head("login.css", title="WWAG Equipment")

print html.make_navbar(loggedIn, userType)
print '<div id="greeting"><h2>{}</h2><div id = "message">'.format(mnm)

if query_success:
    print body
else:
    print message

print """
</div></div>
</body>
</html>
 """
