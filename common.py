def results_as_dicts(cursor):
    """
    Takes a MySQLdb cursor object and returns a list of dictionaries, each representing a row
    returned by the most recent query, with attribute names as keys and values as values
    """
    headings = [tup[0] for tup in cursor.description]
    rows = cursor.fetchall()
    dict_rows = [dict(zip(headings, row)) for row in rows]
    return dict_rows
    
def uniq(l):
    return sorted(list(set(l)))#Cast to set, then back to remove dups