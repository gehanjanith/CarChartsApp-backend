from flask import Blueprint, jsonify, request
from DatabaseModule.database import get_db_connection
import mysql.connector

addUser_blueprint = Blueprint('add-user', __name__)
searchUser_blueprint = Blueprint('search-user', __name__)
updateUser_blueprint = Blueprint('update-user', __name__)
deleteUser_blueprint = Blueprint('delete-user', __name__)


@addUser_blueprint.route('/add-user', methods=['POST'])
def addUser():
    global db_connection, cursor
    data = request.json

    # Define the SQL query
    sql_query = """
    INSERT INTO users (name, email, password, role)
    VALUES (%s, %s, %s, %s)
    """

    try:
        # Get a database connection
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        # Extract values from the data
        values = (
            data.get('name'),
            data.get('email'),
            data.get('password'),
            data.get('role'),
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


@searchUser_blueprint.route('/search-user', methods=['POST'])
def search_user():
    data = request.json
    user_name = data.get('name')

    if user_name:
        try:
            db_connection = get_db_connection()
            cursor = db_connection.cursor(dictionary=True)

            # Example SQL query to search for a user by name
            sql_query = "SELECT * FROM users WHERE name = %s"
            cursor.execute(sql_query, (user_name,))
            user_data = cursor.fetchone()

            if user_data:
                return jsonify(user_data)
            else:
                return jsonify({'error': 'User not found'})

        except mysql.connector.Error as err:
            return jsonify({'error': f'Database error: {err}'})

        finally:
            if 'db_connection' in locals() and db_connection.is_connected():
                cursor.close()
                db_connection.close()

    else:
        return jsonify({'error': 'Invalid request'})


@updateUser_blueprint.route('/update-user/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json

    if user_id and data:
        try:
            db_connection = get_db_connection()
            cursor = db_connection.cursor()

            # Example SQL query to update user data based on user_id
            sql_query = "UPDATE users SET name = %s, email = %s, password = %s, role = %s WHERE id = %s"
            values = (
                data.get('name'),
                data.get('email'),
                data.get('password'),
                data.get('role'),
                user_id
            )
            cursor.execute(sql_query, values)

            db_connection.commit()
            return jsonify({'message': 'User data updated successfully'})

        except mysql.connector.Error as err:
            return jsonify({'error': f'Database error: {err}'})

        finally:
            if 'db_connection' in locals() and db_connection.is_connected():
                cursor.close()
                db_connection.close()

    else:
        return jsonify({'error': 'Invalid request'})


@deleteUser_blueprint.route('/delete-user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global db_connection, cursor

    # Define the SQL query
    sql_query = """
    DELETE FROM users
    WHERE id = %s
    """

    try:
        # Get a database connection
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        # Execute the SQL query
        cursor.execute(sql_query, (user_id,))

        # Commit the changes to the database
        db_connection.commit()

        return jsonify({'message': 'User successfully deleted'})

    except mysql.connector.Error as err:
        # Handle database errors
        return jsonify({'error': f'Database error: {err}'})

    finally:
        # Close the database connection in the finally block
        if 'db_connection' in locals() and db_connection.is_connected():
            cursor.close()
            db_connection.close()
