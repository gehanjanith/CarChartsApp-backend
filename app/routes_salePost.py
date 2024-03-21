from flask import Blueprint, jsonify, request
from DatabaseModule.database import get_db_connection, db_config
import mysql.connector

post_blueprint = Blueprint('post', __name__)
getAllPosts_blueprint = Blueprint('get-all-posts', __name__)
getAllPostsPerUser_blueprint = Blueprint('get-all-posts-per-user', __name__)


@post_blueprint.route('/post', methods=['POST'])
def save_data():
    global db_connection, cursor
    data = request.json

    # Define the SQL query
    sql_query = """
    INSERT INTO local_advertisements (price, phone, make, model, year, edition, city, condi, body_type,
    engine_capacity, fuel_type, mileage, description, user)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    try:
        # Get a database connection
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        # Extract values from the data
        values = (
            data.get('price'),
            data.get('phone'),
            data.get('make'),
            data.get('model'),
            data.get('year'),
            data.get('edition'),
            data.get('city'),
            data.get('condi'),
            data.get('body_type'),
            data.get('engine_capacity'),
            data.get('fuel_type'),
            data.get('mileage'),
            data.get('description'),
            data.get('user')
        )

        # Execute the SQL query
        cursor.execute(sql_query, values)

        # Commit the changes to the database
        db_connection.commit()

        return jsonify({'message': 'Data successfully saved to the database'})

    except mysql.connector.Error as err:
        # Handle database errors
        return jsonify({'error': f'Database error: {err}'})

    finally:
        # Close the database connection in the finally block
        if 'db_connection' in locals() and db_connection.is_connected():
            cursor.close()
            db_connection.close()


@getAllPosts_blueprint.route('/get-all-posts', methods=['GET'])
def get_all_data():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for JSON output

        cursor.execute("SELECT * FROM local_advertisements")
        data = cursor.fetchall()

        return jsonify(data)

    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error'})

    finally:
        cursor.close()
        conn.close()


@getAllPostsPerUser_blueprint.route('/get-all-posts-per-user/<string:user>', methods=['GET'])
def get_all_data_per_user(user):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for JSON output

        query = "SELECT * FROM local_advertisements WHERE user = %s"
        cursor.execute(query, (user,))
        data = cursor.fetchall()

        return jsonify(data)

    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error'})

    finally:
        cursor.close()
        conn.close()
