import mysql
from flask import Blueprint, jsonify, request
from DatabaseModule.database import db_config
from datetime import datetime

login_blueprint = Blueprint('login', __name__)


@login_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    success, role = authenticate_user(username, password)

    if success:
        response = {
            'success': True,
            'message': 'Login successful',
            'role': role
        }
        # Update last_login date in the database
        update_last_login(username)
    else:
        response = {
            'success': False,
            'message': 'Invalid username or password'
        }
    return jsonify(response)


def authenticate_user(username, password):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE name=%s AND password=%s", (username, password))
        user_data = cursor.fetchone()

        if user_data:
            # User found in the database
            role = user_data[4]
            print(role)
            return True, role
        else:
            # User not found or password incorrect
            return False, None

    except Exception as e:
        print(f"Database error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def update_last_login(username):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("UPDATE users SET last_login=%s WHERE name=%s", (current_date, username))
        conn.commit()
    except Exception as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
