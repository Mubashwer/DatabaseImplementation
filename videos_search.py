# The libraries we'll need
import sys, cgi, redirect, session, MySQLdb
from common import *
from html import *
# Get the session and check if logged in
sess = session.Session(expires=60*20, cookie_path='/')
loggedIn = sess.data.get('loggedIn')
userType = sess.data.get('userType')
form = cgi.FieldStorage()

# ---------------------------------------------------------------------------------------------------------------------
# send session cookie
print "%s\nContent-Type: text/html\n" % (sess.cookie)

print make_head("video_modify.css", title = "WWAG Video Search")

print make_navbar(loggedIn, userType)



form_names = ['video_id', 'video_name', 'game_id', 'game_name', 'instance_run_id', 'instance_run_name', 'price', 'video_type']
sql_col_names = ['VideoID', 'VideoName', 'GameID', 'GameName', 'InstanceRunID', 'InstanceName', 'Price', 'VideoType']
form_to_sql = dict(zip(form_names, sql_col_names))
    
form_data = {}
for name in form_names:
    form_data[name] = form.getvalue(name)

print """
<div class="search_form">
<h2 class="header">VIDEOS</h2>
<form action="videos_search.py" method="post">
    <fieldset id="search">
        <legend>Video Search</legend>
        <div class="textbox">
            <label for="video_id">Video ID:</label>
            <input name="video_id" id="video_id" type="text" value="{}"/>
        </div>

        <div class="textbox">
            <label for="video_name">Video Name:</label>
            <input name="video_name" id="video_name" type="text" value="{}"/>
        </div>
        
         <div class="textbox">
            <label for="game_id">Game ID:</label>
            <input name="game_id" id="game_id" type="text" value="{}"/>
        </div>

        <div class="textbox">
            <label for="game_name">Game Name:</label>
            <input name="game_name" id="game_name" type="text" value="{}"/>
        </div>

        <div class="textbox">
            <label for="instance_run_id">InstanceRun ID:</label>
            <input name="instance_run_id" id="instance_run_id" type="text" value="{}"/>
        </div>

        <div class="textbox">
            <label for="instance_run_name">InstanceRun Name:</label>
            <input name="instance_run_name" id="instance_run_name" type="text" value="{}"/>
        </div>

         <div class="textbox">
            <label for="price">Price:</label>
            <input name="price" id="price" type="text" value="{}"/>
        </div>

        <div class="textbox">
            <label for="video_name">Video Type:</label>
            <input name="video_type" id="video_type" type="text" value="{}"/>
        </div>

    </fieldset>
    <div id="buttons" class="button_select">
            <input type="reset" value="Reset" />       
            <input type="submit" value="Submit" />
    </div>
</form>
</div>
""".format(*[form_data[name] if form_data[name] is not None else '' for name in form_names])

db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003g29", "enigma29", "info20003g29", 3306)
cursor = db.cursor()
              
#The query will be made up of several elements, starting select
select_elem = 'SELECT'
              
# These are the columns we wish to select from each table
# select_cols[some_table] = [list, of, columns, from, some_table]
select_cols = {}
select_cols['Video'] = ['VideoID', 'VideoName', 'Price', 'VideoType']
select_cols['Game'] = ['GameID', 'GameName']
select_cols['InstanceRun'] = ['InstanceRunID', 'InstanceName']


#Luckily the column names are unique (except for foreign keys)
#We compile a list of names and then join them to form a string, with commas seperating
all_columns = []

for columns in select_cols.values():
    for column in columns:
        all_columns.append(column)

columns_elem = 'LOWER(VideoName),LOWER(GameName),LOWER(InstanceName),' + ','.join(all_columns)

from_elem = 'FROM'

tables = select_cols.keys()
tables_elem = ' NATURAL JOIN '.join(tables)

where_elem = 'WHERE'

subs = []#list of string substitution to be made into the query
conditions = []
values = []
for (form_name, val) in form_data.items():
    if val:
        if form_name in ['video_name', 'game_name', 'instance_run_name']:
                conditions.append('LOWER({}) LIKE %s'.format(form_to_sql[form_name]))
                subs.append("%" + val.lower() + "%")
        else:
            conditions.append(form_to_sql[form_name] + " LIKE %s")
            subs.append("%" + val + "%")
        values.append(val)
conditions_elem = ' AND '.join(conditions)

query_elems = [select_elem, columns_elem, from_elem, tables_elem]
if conditions:
    query_elems.append(where_elem)
    query_elems.append(conditions_elem)
limit_elem =  'LIMIT 40'   
# Form query by joining it's elements, seperated by spaces, and appending a semicolon and execute it
query = ' '.join(query_elems) + ';'
cursor.execute(query, tuple(subs))
rows = cursor.fetchall()

# print results in table
print '<table class="gridtable" align ="center">'
print '<tr><th>GameID</th><th>GameName</th><th>VideoID</th><th>VideoName</th><th>Price</th><th>VideoType</th><th>InstanceRunID</th><th>InstanceRunName</th></tr>'
for row in rows:
    print '<tr>'
    video_id = row[5];
    for element in row[3:]:#Skip over LOWER(whatever)s when printing
        print '<td><span class="link"><a href="video.py?video_id={}">{}</a></span></td>'.format(video_id, element)
    print '</tr>'
print '</table>'    

print end_html
                
# Tidy up and free resources
sess.close()
