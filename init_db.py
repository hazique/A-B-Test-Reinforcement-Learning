import sqlite3
from os import path

def init():
    if path.exists('database.db'):
        connection = sqlite3.connect('database.db')
    else:
        connection = sqlite3.connect('database.db')

        with open('schema/db.sql') as f:
            connection.executescript(f.read())

        connection.commit()
        connection.close()

if __name__ == "__main__":
    init()