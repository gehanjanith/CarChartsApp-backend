from flask import Blueprint, jsonify, request
from DatabaseModule.database import get_db_connection, db_config
import mysql.connector

comments_blueprint = Blueprint('save-message', __name__)
getComments_blueprint = Blueprint('get-message', __name__)


@comments_blueprint.route('/save-message', methods=['POST'])
def save_message():
    global db_connection, cursor
    data = request.json

    # Define the SQL query
    sql_query = """
       INSERT INTO messages (post_id, msg, user)
       VALUES (%s, %s, %s)
       """

    try:
        # Get a database connection
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        # Extract values from the data
        values = (
            data.get('post_id'),
            data.get('msg'),
            data.get('user'),

        )

        # Execute the SQL query
        cursor.execute(sql_query, values)

        # Commit the changes to the database
        db_connection.commit()

        return jsonify({'message': 'Message successfully saved to the database'})

    except mysql.connector.Error as err:
        # Handle database errors
        return jsonify({'error': f'Database error: {err}'})

    finally:
        # Close the database connection in the finally block
        if 'db_connection' in locals() and db_connection.is_connected():
            cursor.close()
            db_connection.close()


@getComments_blueprint.route('/get-message/<int:post_id>', methods=['GET'])
def get_messages_route(post_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for JSON output

        query = "SELECT * FROM messages WHERE post_id = %s"
        cursor.execute(query, (post_id,))
        data = cursor.fetchall()

        return jsonify(data)

    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error'})

    finally:
        cursor.close()
        conn.close()
