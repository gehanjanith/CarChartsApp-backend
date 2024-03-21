from flask import Blueprint, jsonify, request
from DatabaseModule.database import get_db_connection, db_config
import mysql.connector

userReport_blueprint = Blueprint('users', __name__)
searchRecordsReport_blueprint = Blueprint('search-records', __name__)
vehicleListingsCountReport_blueprint = Blueprint('Vehicle-Listings-Count', __name__)


# MIS Reports
@userReport_blueprint.route("/users", methods=["GET"])
def get_all_users_route():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for JSON output

        cursor.execute("SELECT name, email, role FROM users")
        data = cursor.fetchall()

        return jsonify(data)

    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error'})

    finally:
        cursor.close()
        conn.close()


@searchRecordsReport_blueprint.route('/search-records', methods=['GET'])
def get_search_records():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for JSON output

        cursor.execute("SELECT make, model, minYear, maxYear, timestamp FROM search_records")
        data = cursor.fetchall()

        return jsonify(data)

    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error'})

    finally:
        cursor.close()
        conn.close()


@vehicleListingsCountReport_blueprint.route('/Vehicle-Listings-Count', methods=['GET'])
def get_search_records():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for JSON output

        cursor.execute("SELECT count(*) as count FROM local_advertisements")  # Alias the count(*) column as count
        data = cursor.fetchone()

        return jsonify(data)

    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error'})

    finally:
        cursor.close()
        conn.close()
