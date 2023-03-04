import sqlite3
import json

def initdb():
    connection = sqlite3.connect('database.db')

    with open('schema.sql') as f:
        connection.executescript(f.read())

    cur = connection.cursor()

    cur.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", ('BenPople', 'H4rdw4re', 'popleb@btc.ac.uk'))
    cur.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", ('AbigailCollard', 'H4rdw4re', 'collarda@btc.ac.uk'))

    connection.commit()
    connection.close()