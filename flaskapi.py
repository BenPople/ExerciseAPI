from flask import Flask, request, url_for, flash, redirect, jsonify
from flask_cors import CORS
import sqlite3
import initflaskdb as ifdb

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def SQL_to_json(sql_rows):
    return jsonify([dict(ix) for ix in sql_rows])

@app.route('/api/users/get/all')
def fetch_all_users():
    try:
        conn = get_db_connection()
        return SQL_to_json(conn.execute('SELECT * FROM users').fetchall())
    except:
        return jsonify({"Error" : "No users to return!"})
    finally:
        print(f"Finalising /api/users/get/all")
        conn.close()

@app.route('/api/users/get/byid')
def fetch_user_by_id():
    try:
        userId = request.args.get('id')
        conn = get_db_connection()
        return SQL_to_json(conn.execute('SELECT * FROM users WHERE id=?', userId))
    except:
        return jsonify({"Error" : "User does not exist!"})
    finally:
        print(f"Finalising /api/users/get/byid")
        conn.close()

@app.route('/api/users/login', methods=['POST'])
def login_user():
    #With Swift, we expect POSTed data through type 'application/json' POST not HTML Form POST
    try:
        loginData = request.get_json()
        username = loginData['username']
        password = loginData['password']

        conn = get_db_connection()
        return SQL_to_json(conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)))
    except:
        return jsonify({"Login" : False})
    finally:
        print(f"Finalising /api/users/login")
        conn.close()

@app.route('/api/users/register', methods=['POST'])
def add_new_user():
    #With Swift, we expect POSTed data through type 'application/json' POST not HTML Form POST
    try:
        userData = request.get_json()
        username = userData['username']
        password = userData['password']
        email = userData['email']

        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', (username, password, email))

        return jsonify({"Register_Success" : True})
    except:
        return jsonify({"Register_Success" : False})
    finally:
        print(f"Finalising /api/users/register")
        conn.commit()
        conn.close()



ifdb.initdb()
app.run()



