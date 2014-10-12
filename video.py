# The libraries we'll need
import sys, cgi, redirect, session, MySQLdb

# Get the session and check if logged in
sess = session.Session(expires=60*20, cookie_path='/')
loggedIn = sess.data.get('loggedIn')
form = cgi.FieldStorage()

#TODO db=MySQLdb.connnect(...g09', 'enigma...)

video_id = form.getvalue("video_id")

q0 = "SELECT * FROM Video NATURAL JOIN InstanceRun WHERE VideoID = {};".format(video_id)
db.execute(q0)
res0 = db.store_result()
rows0 = rows_from_res(res0)
instance_id = rows0[0]["InstanceRunID"]

q1 = "SELECT * FROM InstanceRun NATURAL JOIN InstancePlayer NATURAL JOIN Player WHERE\
InstanceRunID = {};".format(instance_id)
q2 = "SELECT * FROM Video NATURAL JOIN Game WHERE VideoID = {};".format(video_id)
q3 = "SELECT * FROM Equipment NATURAL JOIN InstanceEquipment\
NATURAL JOIN InstanceRun WHERE InstanceRunId = {};".format(instance_id)

queries = [q0,q1,q2,q3]
#Corresponding to [video/instance, player, game, equipment]

for query in queries:
    db.execute(query)
    result = db.store_result()
    results.append(result)
    all_rows.append(rows_from_res(result))
    
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
#TODO: print relevant info from 4 queries and add order button, with possible access code input,
#conditional on viewer type
#Print Video info
video_info = []

video_info.append("Name: " + all_rows[0][0]["VideoName"])
video_type = all_rows[0][0]["VideoType"]
video_info.append("Type: " + video_type)
video_info.append("Price: " + all_rows[0][0]["Price"])
url = all_rows[0][0]["URL"]
if (video_type in ["Non-Premium", "Free"]):
    video_info.append("Url: " + wrap_link(url, url))

video_html = ""
for info in video_infos:
    video_html += wrap_p(info, str(video_info.index(info)))
video_html = wrap_div(video_html, div_id="video_info")

print(video_html)

#Print Player info
players = uniq(get_all(col_name = "UserName", query_index = 1))

player_html = wrap_tr(wrap(td("Participating Players:")))
for player in players:
    #TODO wrap players in <a>s to link to player info page
    player_html += wrap_tr(wrap_td(player))
player_html = wrap_div(wrap_table(player_html), 'player_info')

print(player_html)

#Print Game info
#TODO add link  to game info page
game_name = all_rows[2][0]["GameName"]
print(wrap_div(wrap_p("Game: " + game_name)))

#Print equipment info
equipments = get_all(col_name = "ModelAndMake", query_index = 3)
equipment_html = wrap_tr(wrap(td("Equipment Used:")))
for equipment in equipments:
    #TODO wrap equipments in <a>s to link to equipment info page
    equipment_html += wrap_tr(wrap_td(equipment))
equipment_html = wrap_div(wrap_table(equipment_html), div_id = 'equipment_info')
print(equipment_html)

#Print InstanceRun info

ir_info = []

ir_info.append("Instance Run Details:")
ir_info.append("Name: " + all_rows[1][0]["InstanceName"])
ir_info.append("Recorded time: " + all_rows[1][0]["RecordedTime"])
ir_info.append("Category name: " + all_rows[1][0]["CategoryName"])

ir_html =""
for line in ir_info:
    ir_html += wrap_p(line)
ir_html = wrap_div(ir_html, div_id = "instance_run_info")

print(ir_html)

### HELPERS ###
def rows_from_res(res):
    return res.fetch_row(max_rows = 0, how = 1)
    #Get all rows, with each row as a dictionary with column names as keys and values as values

def get_all(col_name = None, query_index = None):
    [row[col_name] for row in all_rows[query_index]]
    #Get the value in that column, for each row in the rows returned by the query with index
    # query_index
    
def uniq(l):
    return sorted(list(set(l)))#Cast to set, then back to remove dups

def wrap_p(text, p_id=None):
    if p_id:
        return "<p id='{}'>".format(p_id) + text + "</p>\n"
    else:
        return "<p>" + text + "</p>\n"

def wrap_link(text, href=None):
    return "<a href='{}'>".format(href) + text + "</a>"

def wrap_tr(text):
    return "<tr>" + text + "</tr>\n"

def wrap_td(text):
    return "<td>" + text + "</td>"

def wrap_table(text):
    return "<table>\n" + text + "\n</table>\n"
