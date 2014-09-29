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
#TODO: not using radio buttons yet
#Create a dictionary to map names used in HTML form to their corresponding MySQL database attribute names
form_names = ['video_id', 'game_id', 'game_name', 'instance_run_id', 'instance_run_name', 'price']
sql_col_names = ['VideoID', 'GameID', 'GameName', 'InstanceRunID', 'InstanceName', 'Price']
form_to_sql = dict(zip(form_names, sql_col_names))
    
form_data = {}
for name in form_names:
    form_data[name] = form.getvalue(name)
        
#TODO: connect to the correct database
#db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003", "cisds", "info20003", 3306)
#cur = db.cursor()
              
#The query will be made up of several elements, starting select
select_elem = 'SELECT'
              
# These are the columns we wish to select from each table
# select_cols[some_table] = [list, of, columns, from, some_table]
select_cols = {}
select_cols['Video'] = ['VideoID', 'URL', 'Price', 'VideoType']
select_cols['Game'] = ['GameID', 'GameName']
select_cols['InstanceRun'] = ['InstanceRunID', 'InstanceName']


#Luckily the column names are unique (except for foreign keys)
#We compile a list of names and then join them to form a string, with commas seperating
all_columns = []

for columns in select_cols.values():
    for column in columns:
        all_columns.append(column)

columns_elem = ','.join(all_columns)

from_elem = 'FROM'

tables = select_cols.keys()
tables_elem = ' NATURAL JOIN '.join(tables)

where_elem = 'WHERE'

#TODO add where clauses to conditions_s (based on form data, using like '%term%'
# convert term to lower case before query? any other parsing?
conditions = []
for (form_name, val) in form_data.items():
    if val:
        conditions.append(form_to_sql[form_name] + " LIKE '%" + val + "%'") 

conditions_elem = ' AND '.join(conditions)

query_elems = [select_elem, columns_elem, from_elem, tables_elem]
if conditions:
    query_elems.append(where_elem)
    query_elems.append(conditions_elem)
    
# Form query by joining it's elements, seperated by spaces, and appending a semicolon
query = ' '.join(query_elems) + ';'

print query
#TODO: execute query and return results
print """
</body>
</html>
"""

# Tidy up and free resources
sess.close()​​​
