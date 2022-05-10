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
              WHERE sub_id = ?'''
    cur.execute(sql, data)
    close_connection(connection)

def get_participant_count():
    connection = get_connection()
    cur = connection.cursor()
    sql = ''' select count(*) from rl_test'''
    cur.execute(sql)
    count = cur.fetchall()[0]
    close_connection(connection)
    return count


def get_stored_rewards_log():
    connection = get_connection()
    cur = connection.cursor()

    sql = "select variant, result, test_done from rl_test"
    cur.execute(sql)
    rows = cur.fetchall()
    close_connection(connection)
    return rows

def get_record_count_for_variant(variant):
    connection = get_connection()
    cur = connection.cursor()

    sql = "select count(*) from rl_test where variant=?"
    cur.execute(sql, str(variant))

    count = cur.fetchall()[0][0]
    close_connection(connection)
    return count
