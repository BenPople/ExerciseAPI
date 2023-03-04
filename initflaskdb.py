import sqlite3
import hashlib

HASH_SALT = "L6SmartAppDevelopment"

def initdb():
    connection = sqlite3.connect('database.db')

    with open('schema.sql') as f:
        connection.executescript(f.read())

    cur = connection.cursor()

    cur.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                ('BenPople', hashlib.md5(('H4rdw4re' + HASH_SALT).encode()).hexdigest(), 'popleb@btc.ac.uk'))
    
    cur.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                ('AbigailCollard', hashlib.md5(('H4rdw4re' + HASH_SALT).encode()).hexdigest(), 'collarda@btc.ac.uk'))

    connection.commit()
    connection.close()