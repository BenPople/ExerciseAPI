import sqlite3
import hashlib
import random
import datetime

HASH_SALT = "L6SmartAppDevelopment"

def initdb():
    connection = sqlite3.connect('database.db')

    with open('schema.sql') as f:
        connection.executescript(f.read())

    cur = connection.cursor()

    #Insert example users
    cur.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                ('BenPople', hashlib.md5(('H4rdw4re' + HASH_SALT).encode()).hexdigest(), 'popleb@btc.ac.uk'))
    
    cur.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                ('SimonWest', hashlib.md5(('H4rdw4re' + HASH_SALT).encode()).hexdigest(), 'wests@btc.ac.uk'))

    cur.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            ('EmilyWang', hashlib.md5(('p@ssword1' + HASH_SALT).encode()).hexdigest(), 'emilyw@xyz.com'))

    cur.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                ('MikeSmith', hashlib.md5(('myPa$$w0rd' + HASH_SALT).encode()).hexdigest(), 'mikes@abc.com'))

    cur.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                ('AliceJones', hashlib.md5(('secret12' + HASH_SALT).encode()).hexdigest(), 'alicej@def.com'))

    cur.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                ('BobLee', hashlib.md5(('qwerty123' + HASH_SALT).encode()).hexdigest(), 'bobl@ghi.com'))

    #Insert example excersise types
    cur.execute("INSERT INTO exercisetypes (name, description) VALUES (?, ?)",
            ('Running', 'A cardiovascular exercise that involves running or jogging.'))

    cur.execute("INSERT INTO exercisetypes (name, description) VALUES (?, ?)",
                ('Weightlifting', 'An exercise that involves lifting weights to build strength and muscle mass.'))

    cur.execute("INSERT INTO exercisetypes (name, description) VALUES (?, ?)",
                ('Swimming', 'A low-impact exercise that involves swimming laps in a pool or other body of water.'))

    cur.execute("INSERT INTO exercisetypes (name, description) VALUES (?, ?)",
                ('Yoga', 'A series of postures and breathing exercises designed to promote relaxation and flexibility.'))

    cur.execute("INSERT INTO exercisetypes (name, description) VALUES (?, ?)",
                ('Cycling', 'A cardiovascular exercise that involves cycling on a stationary or moving bike.'))

    #Insert example excersise activities
    #Define a list of user IDs and exercise type IDs
    user_ids = [1, 2, 3, 4, 5]
    exercise_type_ids = [1, 2, 3, 4, 5]

    #Generate 100 random exercise entries
    for i in range(100):
        #Select a random user ID and exercise type ID
        user_id = random.choice(user_ids)
        exercise_type_id = random.choice(exercise_type_ids)
        
        #Generate a random duration between 10 and 60 minutes
        duration_minutes = random.randint(10, 60)
        
        #Generate a random date within the last 30 days
        days_ago = random.randint(0, 30)
        date_completed = datetime.date.today() - datetime.timedelta(days=days_ago)
        
        #Insert the new exercise entry into the exercises table
        cur.execute("INSERT INTO exercises (user_id, exercisetype_id, duration_minutes, date_completed) VALUES (?, ?, ?, ?)",
                    (user_id, exercise_type_id, duration_minutes, date_completed))

    connection.commit()
    connection.close()