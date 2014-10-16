# The libraries we'll need
import sys, cgi, MySQLdb, warnings, hashlib, uuid

warnings.filterwarnings('error', category=MySQLdb.Warning)

# generic function for insert into MySQL db table
def insert(db, cursor, table, fields, keys):
    query = '''INSERT INTO {} VALUES ('''.format(table)
    args = ()
    
    for key in keys:
        if fields[key] == None:
            query += "DEFAULT, "
        else:
            query += "%s, "
            args += (fields[key],)
    query = query[:-2] + ");"    
    
    try:   
        cursor.execute(query, args)
        db.commit()
        return '<div class = "success">Insert Successful!</div>'
    except Exception, e:
        return '<div class = "error">Insert Error! {}.</div>'.format(repr(e))

# generic function for update in MySQL db table    
def update(db, cursor, table, fields, keys, pk, ignore=[]):    
    query = "UPDATE {} SET ".format(table) 
    args = ()
    
    # add conditions (primary keys to identify row)
    for key in keys:
        if key not in ignore:
            query += "{} = %s, ".format(key)
            args += (fields[key],)
        
    # add conditions (primary keys to identify row)
    condition = " WHERE "    
    for key in pk:
        condition += "{} = %s AND ".format(key)
        args += (fields[key],)
    query = query[:-2] + condition[:-4] + ";"

    try:   
        cursor.execute(query, args)
        db.commit()
        return '<div class = "success">Update Successful!</div>'
    except Exception, e:
        return '<div class = "error">Update Error! {}.</div>'.format(repr(e))     
    
# generic function for delete in MySQL db table    
def delete(db, cursor, table, fields, pk):
    query = '''DELETE FROM {0} '''.format(table)
    condition = "WHERE " 
    args = ()
    
    # add conditions (primary keys to identify row)
    for key in pk:
        condition += "{} = %s AND ".format(key)
        args += (fields[key],)
    query += condition[:-4]
    
    try:   
        cursor.execute(query, args)
        db.commit()
        return '<div class = "success">Delete Successful!</div>'
    except Exception, e:        
        return '<div class = "error">Delete Error! {}.</div>'.format(repr(e))


# generic function for search in MySQL db table (single table only)
def search(db, cursor, table, fields, keys, exact_keys, select=[], ignore=[], limit=0, fetch_one=False):
    query = '''SELECT * FROM {} '''.format(table)
    vars = ""
    
    # add select variables if all of them are not required
    for key in select:
        vars += key + ", " 
    if len(select):
        query = query[:7] + vars[:-2] + query[8:]

    # add conditions with "like" and "=" and ignore some (e.g password, salt)
    condition = "WHERE "
    args = ()                                                                                    
    for key in keys:
        if fields[key] != None:                                                                                     
            if key in ignore:
                continue;
            if key in exact_keys:
                condition += "{} = %s AND ".format(key)
                args += (fields[key],)
            else:
                condition += "{} LIKE %s AND ".format(key)                                                                                          
                args += ("%" + fields[key] + "%",)
                                                                                                    
    if len(args):
        query += condition[:-4]
    
    # add limit if given
    if limit:
        query += "LIMIT {};".format(limit)
        
    try:   
        cursor.execute(query, args)
        if fetch_one:
            return (cursor.fetchone(), "")
        else:
            return (cursor.fetchall(), "")
    except Exception, e:   
        return(None, '<div class = "error">Search Error! {}.</div>'.format(repr(e)));    
