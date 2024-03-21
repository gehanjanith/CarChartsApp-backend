from flask import Blueprint, jsonify, request
from DatabaseModule.database import get_db_connection, db_config
import mysql.connector

appraisalRequest_blueprint = Blueprint('appraisal-request', __name__)
getAllAppraisals_blueprint = Blueprint('get-all-appraisals', __name__)
valuationResponse_blueprint = Blueprint('add-valuation', __name__)
appraisalPerUser_blueprint = Blueprint('appraisal_per_user', __name__)
getAllNewAppraisals_blueprint = Blueprint('get-all-new-appraisals', __name__)


# getAllPostsPerUser_blueprint = Blueprint('get-all-posts-per-user', __name__)

@appraisalRequest_blueprint.route('/appraisal-request', methods=['POST'])
def save_data():
    global db_connection, cursor
    data = request.json

    # Define the SQL query
    sql_query = """
    INSERT INTO appraisal_requests (make, model, year, edition, condi, body_type,
    engine_capacity, fuel_type, mileage, description, user)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    try:
        # Get a database connection
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        # Extract values from the data
        values = (
            data.get('make'),
            data.get('model'),
            data.get('year'),
            data.get('edition'),
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


@getAllAppraisals_blueprint.route('/get-all-appraisals', methods=['GET'])
def get_all_data():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for JSON output

        cursor.execute("SELECT * FROM appraisal_requests")
        data = cursor.fetchall()

        return jsonify(data)

    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error'})

    finally:
        cursor.close()
        conn.close()


@valuationResponse_blueprint.route('/add-valuation/<appraisal_id>', methods=['PUT'])
def add_valuation(appraisal_id):
    try:
        # Extract data from the request
        data = request.get_json()
        valuation = data.get('valuation')
        comments = data.get('comment')
        appraiser = data.get('appraiser')
        print('data', data)

        # Update the appraisal record with valuation and comments
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE appraisal_requests SET valuation = %s, comments = %s, appraised_date = CURRENT_TIMESTAMP, appraiser = %s WHERE id = %s",
            (valuation, comments, appraiser, appraisal_id))
        conn.commit()
        return jsonify({'success': True, 'message': 'Valuation and comments added successfully'})
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({'success': False, 'message': 'Error adding valuation and comments'})
    finally:
        cursor.close()
        conn.close()


@appraisalPerUser_blueprint.route('/get-all-appraisal-per-user/<username>', methods=['GET'])
def get_all_appraisal_per_user(username):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for JSON output

        cursor.execute("SELECT * FROM appraisal_requests WHERE user = %s", (username,))
        appraisal_listings = cursor.fetchall()

        return jsonify(appraisal_listings)

    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error'})

    finally:
        cursor.close()
        conn.close()


@getAllNewAppraisals_blueprint.route('/get-all-new-appraisals', methods=['GET'])
def get_all_data():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for JSON output

        # Modify the SQL query to retrieve messages only if the valuation field is empty
        cursor.execute("SELECT * FROM appraisal_requests WHERE valuation IS NULL OR valuation = ''")
        data = cursor.fetchall()

        return jsonify(data)

    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error'})

    finally:
        cursor.close()
        conn.close()
