# The libraries we'll need
import sys, cgi, redirect, session, MySQLdb

# Get the session and check if logged in
sess = session.Session(expires=60*20, cookie_path='/')
loggedIn = sess.data.get('loggedIn')
form = cgi.FieldStorage()

#TODO db=MySQLdb.connnect(...)

video_id = form.getvalue("video_id")

q0 = "SELECT * FROM Video NATURAL JOIN InstanceRun WHERE VideoID = {};".format(video_id)
db.execute(q0)
res0 = db.store_result()
rows0 = rows_from_res(res0)
instance_id = rows0[0]["InstanceRunID"]

q1 = "SELECT * FROM InstanceRun NATURAL JOIN InstancePlayer NATURAL JOIN Player WHERE\
InstanceRunID = {};".format(instance_id)

q2 = "SELECT * FROM Video NATURAL JOIN Game WHERE VideoID = {};".format(video_id)
queries = [q0,q1,q2]

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
