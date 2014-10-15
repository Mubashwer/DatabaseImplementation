# The libraries we'll need
import sys, cgi, redirect, session, MySQLdb
from common import *

# Get the session and check if logged in
sess = session.Session(expires=60*20, cookie_path='/')
loggedIn = sess.data.get('loggedIn')
form = cgi.FieldStorage()
# ---------------------------------------------------------------------------------------------------------------------

db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003g29", "enigma29", "info20003g29", 3306)
c = db.cursor()

video_id = form.getvalue("video_id")
#If video_id is not set: redirect to videos_search
if not video_id:
    print "Status: 307 Temporary Redirect"
    print "Location: videos_search.py" 

# Each query is pieced together out of a template and some substitutions
templates = []
subs = []

templates.append("SELECT * FROM Video NATURAL JOIN InstanceRun WHERE VideoID = %s")
subs.append((video_id,))
c.execute(templates[0], subs[0])
all_rows = [results_as_dicts(c)] # With more lists of rows to come
instance_id = all_rows[0][0]["InstanceRunID"]

templates.append("select * from Player inner join InstanceRun inner join InstancePlayer \
on InstanceRun.InstanceRunID = InstancePlayer.InstanceRunID \
AND Player.PlayerID = InstancePlayer.PlayerID \
where InstanceRun.InstanceRunID = %s")
subs.append((instance_id,))

templates.append("SELECT * FROM Video NATURAL JOIN Game WHERE VideoID = %s")
subs.append((video_id,))

templates.append("SELECT * FROM Equipment NATURAL JOIN InstanceEquipment \
NATURAL JOIN InstanceRun WHERE InstanceRunId = %s")
subs.append((instance_id,))

queries = [{'template':templates[i], 'subs':subs[i]} for i in range(4)]

#(q0 has already been run)
for query in queries[1:]:
    c.execute(query['template'], query['subs'])
    all_rows.append(results_as_dicts(c))  

"""
Data returned by any query in list queries can now be accessed using it's index (e.g. 1 for q1)
The general format is all_rows[query_index][row_index]["ColumnName"]
Examples:

To access the value in the UserName column of the fourth row (list index 3) returned by q1:
    all_rows[1][3]["UserName"]

To get a list of all usernames, in the order returned by q1:
    get_all(col_name = "UserName", query_index = 1)
or just
    get_all("UserName", 1)

To get a unique, alphabetically sorted list of usernames, call uniq on the list returned above:
    uniq(get_all("UserName", 1))

"""
# ---------------------------------------------------------------------------------------------------------------------
# send session cookie and put in the basic html
print "%s\nContent-Type: text/html\n" % (sess.cookie)
print make_head(title = 'WWAG: ' + all_rows[0][0]["VideoName"])
print make_navbar()

#Print Video info
video_info = []

video_info.append("Name: " + all_rows[0][0]["VideoName"])
video_type = all_rows[0][0]["VideoType"]
video_info.append("Type: " + video_type)
video_info.append("Price: $" + str(all_rows[0][0]["Price"]))
url = all_rows[0][0]["URL"]

if (video_type in ["Non-Premium", "Free"]):
    video_info.append("Url: " + wrap_link(url, href = url))
else:
    order_html = wrap_div("<input type='submit' value='Order' />",div_id="order_button")
    user_type = sess.data.get("userType")
    if user_type not in ['P','B','S']:
        order_html += 'Access code: <input type="text" name="access_code" />'
    order_html = wrap_div(wrap_form(order_html, \
                          action = 'order.py?video_id={}'.format(video_id)),\
                          div_id="order_form")
    if loggedIn and user_type != 'S':
        print order_html

video_html = ""
for info in video_info:
    video_html += wrap_p(info, str(video_info.index(info)))
video_html = wrap_div(video_html, div_id="video_info")

print(video_html)

#Print Player info

player_html = wrap_tr(wrap_td("Participating Players:"))    

players = uniq([row["UserName"] for row in all_rows[1]])

for player in players:
    player_html += wrap_tr(wrap_td(wrap_link(player, href = 'player_info.py?username=' + player)))
       
player_html = wrap_div(wrap_table(player_html), 'player_info')

print(player_html)

#Print Game info
game_name = all_rows[2][0]["GameName"]
game_id = all_rows[2][0]["GameID"]
print(wrap_div(wrap_p("Game: " + wrap_link(game_name, href = 'game_info.py?game_id=' + str(game_id)))))

#Print equipment info
equipments = uniq([row["ModelAndMake"] for row in all_rows[3]])

equipment_html = wrap_tr(wrap_td("Equipment Used:"))
for equipment in equipments:
    equipment_html += wrap_tr(wrap_td(wrap_link(equipment, href = 'equipment_info.py?mnm='+equipment)))
equipment_html = wrap_div(wrap_table(equipment_html), div_id = 'equipment_info')
print(equipment_html)

#Print InstanceRun info

ir_info = []

ir_info.append("Instance Run Details:")
ir_info.append("Name: " + all_rows[0][0]["InstanceName"])
ir_info.append("Recorded time: " + str(all_rows[0][0]["RecordedTime"]))
ir_info.append("Category name: " + all_rows[0][0]["CategoryName"])

ir_html =""
for line in ir_info:
    ir_html += wrap_p(line)
ir_html = wrap_div(ir_html, div_id = "instance_run_info")

print(ir_html)

print end_html
​
