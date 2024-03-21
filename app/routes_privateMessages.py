from flask import Blueprint, jsonify, request
from DatabaseModule.database import get_db_connection, db_config
import mysql.connector

savePrivateMessage_blueprint = Blueprint('save-private-message', __name__)
getPrivateMessages_blueprint = Blueprint('get-private-messages', __name__)
getUserPrivateMessages_blueprint = Blueprint('get-user-private-messages', __name__)
getPrivateMessagesPerAdvertisement_blueprint = Blueprint('get-advertisement-private-messages', __name__)
getAdvertisementPrivateMessagesPerUser_blueprint = Blueprint('get-advertisement-private-messages-per-user', __name__)


# private messages
@savePrivateMessage_blueprint.route('/save-private-message', methods=['POST'])
def save_private_message():
    global db_connection, cursor
    data = request.json

    # Define the SQL query
    sql_query = """
       INSERT INTO private_messages (post_id, msg, user,receiver)
       VALUES (%s, %s, %s, %s)
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
            data.get('receiver'),

        )
        # Execute the SQL query
        cursor.execute(sql_query, values)

        # Commit the changes to the database
        db_connection.commit()
        return jsonify({'message': 'Priavte Message successfully saved to the database'})

    except mysql.connector.Error as err:
        # Handle database errors
        return jsonify({'error': f'Database error: {err}'})
    finally:
        # Close the database connection in the finally block
        if 'db_connection' in locals() and db_connection.is_connected():
            cursor.close()
            db_connection.close()


@getPrivateMessages_blueprint.route('/get-private-messages/<string:user>', methods=['GET'])
def get_private_messages_route(user):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for JSON output

        query = "SELECT * FROM private_messages WHERE user = %s"
        cursor.execute(query, (user,))
        data = cursor.fetchall()

        return jsonify(data)

    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error'})

    finally:
        cursor.close()
        conn.close()


@getUserPrivateMessages_blueprint.route('/get-user-private-messages/<int:post_id>/<string:user>/<string:owner>',
                                        methods=['GET'])
def get_private_messages_per_post_route(post_id, user, owner):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for JSON output

        query = "SELECT * FROM private_messages WHERE post_id = %s AND (user = %s OR user = %s )"

        cursor.execute(query, (post_id, user, owner))
        data = cursor.fetchall()

        return jsonify(data)

    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error'})

    finally:
        cursor.close()
        conn.close()


@getPrivateMessagesPerAdvertisement_blueprint.route('/get-advertisement-private-messages/<int:post_id>',
                                                    methods=['GET'])
def get_private_messages_per_advertisement_route(post_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for JSON output

        query = "SELECT * FROM private_messages WHERE post_id = %s "

        cursor.execute(query, (post_id,))
        data = cursor.fetchall()

        return jsonify(data)

    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error'})

    finally:
        cursor.close()
        conn.close()


@getAdvertisementPrivateMessagesPerUser_blueprint.route(
    '/get-advertisement-private-messages-per-user/<int:post_id>/<string:user>/<string:receiver>', methods=['GET'])
def get_private_messages_per_post_per_user_route(post_id, user, receiver):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for JSON output

        query = "SELECT * FROM private_messages WHERE post_id = %s AND (user = %s AND receiver = %s) OR post_id = %s AND (user = %s AND receiver = %s)"

        cursor.execute(query, (post_id, user, receiver, post_id, receiver, user))

        data = cursor.fetchall()

        return jsonify(data)

    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error'})

    finally:
        cursor.close()
        conn.close()
