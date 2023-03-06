from flask import Flask, request, jsonify
from flask_cors import CORS
import initflaskdb as ifdb
import sqlite3
import hashlib

exerciseapp = Flask(__name__)
CORS(exerciseapp)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def SQL_to_json(sql_rows):
    return jsonify([dict(ix) for ix in sql_rows])

@exerciseapp.route('/api/users/get/all')
def fetch_all_users():
    try:
        conn = get_db_connection()
        return SQL_to_json(conn.execute('SELECT * FROM users').fetchall())
    except:
        return jsonify({"Error" : "No users to return!"})
    finally:
        print(f"Finalising /api/users/get/all")
        conn.close()

@exerciseapp.route('/api/users/get/byid')
def fetch_user_by_id():
    try:
        userId = request.args.get('id')
        conn = get_db_connection()
        return SQL_to_json(conn.execute('SELECT * FROM users WHERE id=?',
                                        userId))
    except:
        return jsonify({"Error" : "User does not exist!"})
    finally:
        print(f"Finalising /api/users/get/byid")
        conn.close()

@exerciseapp.route('/api/users/login', methods=['POST'])
def login_user():
    #With Swift, we expect POSTed data through type 'application/json' POST not HTML Form POST
    #Let us current assume we're hashing server side...
    try:
        loginData = request.get_json()
        username = loginData['username']
        password = hashlib.md5((loginData['password'] + HASH_SALT).encode()).hexdigest()

        conn = get_db_connection()
        return SQL_to_json(conn.execute('SELECT * FROM users WHERE username = ? AND password = ?',
                                        (username, password)))
    except:
        return jsonify({"Login" : False})
    finally:
        print(f"Finalising /api/users/login")
        conn.close()

@exerciseapp.route('/api/users/register', methods=['POST'])
def add_new_user():
    #With Swift, we expect POSTed data through type 'application/json' POST not HTML Form POST
    #Let us current assume we're hashing server side...
    try:
        userData = request.get_json()
        username = userData['username']
        password = hashlib.md5((userData['password'] + HASH_SALT).encode()).hexdigest()
        email = userData['email']

        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                     (username, password, email))

        return jsonify({"Register_Success" : True})
    except:
        return jsonify({"Register_Success" : False})
    finally:
        print(f"Finalising /api/users/register")
        conn.commit()
        conn.close()

@exerciseapp.route('/api/exercises/types/get/all')
def fetch_all_exercise_types():
    try:
        conn = get_db_connection()
        return SQL_to_json(conn.execute('SELECT * FROM exercisetypes').fetchall())
    except:
        return jsonify({"Error" : "No exercise types to return!"})
    finally:
        print(f"Finalising /api/exercisetypes/get/all")
        conn.close()

@exerciseapp.route('/api/exercises/activities/get/all')
def fetch_all_exercises():
    try:
        conn = get_db_connection()
        return SQL_to_json(conn.execute('SELECT * FROM exercises').fetchall())
    except:
        return jsonify({"Error" : "No exercises to return!"})
    finally:
        print(f"Finalising /api/exercises/get/all")
        conn.close()

@exerciseapp.route('/api/exercises/activities/add', methods=['POST'])
def add_new_exercise():
    # With Swift, we expect POSTed data through type 'application/json' POST not HTML Form POST
    try:
        exerciseData = request.get_json()
        user_id = exerciseData['user_id']
        exercisetype_id = exerciseData['exercisetype_id']
        duration_minutes = exerciseData['duration_minutes']
        date_completed = exerciseData['date_completed']

        conn = get_db_connection()
        conn.execute('INSERT INTO exercises (user_id, exercisetype_id, duration_minutes, date_completed) VALUES (?, ?, ?, ?)',
                     (user_id, exercisetype_id, duration_minutes, date_completed))

        return jsonify({"Add_Success": True})
    except:
        return jsonify({"Add_Success": False})
    finally:
        print(f"Finalising /api/exercises/add")
        conn.commit()
        conn.close()

@exerciseapp.route('/api/exercises/get/byuserid')
def fetch_exercises_by_user_id():
    try:
        user_id = request.args.get('userid')
        conn = get_db_connection()
        exercises = conn.execute('SELECT * FROM exercises WHERE user_id = ?', (user_id)).fetchall()
        if len(exercises) == 0:
            return jsonify({"Error" : "No exercises found for the specified user ID!"})
        else:
            return SQL_to_json(exercises)
    except:
        return jsonify({"Error" : "An error occurred while fetching exercises by user ID!"})
    finally:
        print(f"Finalising /api/exercises/get/byuserid")
        conn.close()

@exerciseapp.route('/api/exercises/get/details/byuserid')
def fetch_exercise_details_by_user_id():
    try:
        user_id = request.args.get('userid')
        conn = get_db_connection()
        results = conn.execute('SELECT exercisetypes.name, users.username, exercises.duration_minutes, exercises.date_completed FROM exercises \
                                INNER JOIN exercisetypes ON exercises.exercisetype_id = exercisetypes.id \
                                INNER JOIN users ON exercises.user_id = users.id \
                                WHERE exercises.user_id = ?', (user_id,)).fetchall()
        if len(results) == 0:
            return jsonify({"Error" : "No exercises found for the specified user ID!"})
        else:
            exercise_details = []
            for result in results:
                exercise_details.append({'exercise_name': result[0], 'user_name': result[1], 'duration_minutes': result[2], 'date_completed': result[3]})
            return jsonify({"exercise_details": exercise_details})
    except:
        return jsonify({"Error" : "An error occurred while fetching exercise details by user ID!"})
    finally:
        print(f"Finalising /api/exercises/get/details/byuserid")
        conn.close()

@exerciseapp.route('/api/users/get/id/byusername')
def fetch_user_id_by_username():
    try:
        username = request.args.get('username')
        conn = get_db_connection()
        result = conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
        if result is None:
            return jsonify({"Error" : "No user found for the specified username!"})
        else:
            return jsonify({"user_id": result[0]})
    except:
        return jsonify({"Error" : "An error occurred while fetching user ID by username!"})
    finally:
        print(f"Finalising /api/users/get/id/byusername")
        conn.close()

if __name__ == '__main__':
    ifdb.initdb()
    exerciseapp.run()