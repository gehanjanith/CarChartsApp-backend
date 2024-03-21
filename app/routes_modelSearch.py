import mysql
import requests
from flask import Blueprint, jsonify, request
from bs4 import BeautifulSoup
from datetime import datetime

from DatabaseModule.database import db_config

searchVehicle_blueprint = Blueprint('searchVehicle', __name__)


@searchVehicle_blueprint.route("/searchVehicle/<make>/<model>/<year>", methods=["GET"])
def search_vehicle(make, model, year):
    conn = None
    cursor = None
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Execute the MySQL query to retrieve car data
        cursor.execute("SELECT * FROM price_sentiment WHERE make = %s AND model = %s AND year = %s",
                       (make, model, year))
        car_data = cursor.fetchall()

        # Return the car data as JSON response
        return jsonify(car_data)
    except Exception as e:
        # Return error message if an exception occurs
        return jsonify({'error': str(e)})
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()
