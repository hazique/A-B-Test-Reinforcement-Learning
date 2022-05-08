import sqlite3

def get_connection():
    connection = sqlite3.connect('database.db')
    return connection

def close_connection(connection):
    connection.commit()
    connection.close()

def db_has_sub_id(sub_id):
    connection = get_connection()
    cur = connection.cursor()
    cur.execute("select sub_id from rl_test")

    rows = cur.fetchall()
    close_connection(connection)
    if sub_id in rows:
        return True
    else:
        return False

def add_subject_to_table(data):
    connection = get_connection()
    cur = connection.cursor()
    sql = '''INSERT INTO rl_test (sub_id, fname, lname, test_name, variant, test_done) 
            VALUES (?, ?, ?, ?, ?, ?)'''
    
    cur.execute(sql, data)
    
    close_connection(connection)

def update_sub_test_result(data):
    connection = get_connection()
    cur = connection.cursor()

    sql = ''' UPDATE rl_test
              SET result = ?,
                test_done = ?
              WHERE id = ?'''

    cur.execute(sql, data)
    close_connection(connection)
