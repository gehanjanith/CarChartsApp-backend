import mysql
from flask import Blueprint, jsonify

from DatabaseModule.database import db_config

modelReport_blueprint = Blueprint('model-report', __name__)

#
# @modelReport_blueprint.route("/model-report", methods=["GET"])
# def model_report():
#     conn = None
#     cursor = None
#     try:
#         # Connect to the database
#         conn = mysql.connector.connect(**db_config)
#         cursor = conn.cursor(dictionary=True)
#
#         # Execute the MySQL query to retrieve car data
#         cursor.execute("SELECT * FROM price_sentiment",)
#         car_data = cursor.fetchall()
#
#         # Return the car data as JSON response
#         return jsonify(car_data)
#     except Exception as e:
#         # Return error message if an exception occurs
#         return jsonify({'error': str(e)})
#     finally:
#         # Close the cursor and connection
#         if cursor:
#             cursor.close()
#         if conn:
#             conn.close()

from flask import jsonify

# @modelReport_blueprint.route("/model-report", methods=["GET"])
# def model_report():
#     conn = None
#     cursor = None
#     try:
#         # Connect to the database
#         conn = mysql.connector.connect(**db_config)
#         cursor = conn.cursor(dictionary=True)
#
#         # Retrieve distinct make, model, and year combinations
#         cursor.execute("SELECT DISTINCT make, model, year FROM makes")
#         make_model_year_combinations = cursor.fetchall()
#
#         # Initialize list to store model reports
#         model_reports = []
#
#         # Iterate over each make, model, and year combination
#         for make_model_year in make_model_year_combinations:
#             make = make_model_year['make']
#             model = make_model_year['model']
#             years = make_model_year['year'].split(',')
#
#             # Iterate over each year for the current make and model
#             for year in years:
#                 # Query to get the last min, max, and average prices for the specific year
#                 cursor.execute("""
#                     SELECT * FROM price_sentiment
#                     WHERE make = %s AND model = %s AND year = %s
#                     ORDER BY date DESC
#                     LIMIT 1
#                 """, (make, model, year))
#                 result = cursor.fetchone()
#
#                 # If result is not empty, append to model reports
#                 if result:
#                     model_reports.append(result)
#
#         # Return the model reports as JSON response
#         return jsonify(model_reports)
#     except Exception as e:
#         # Return error message if an exception occurs
#         return jsonify({'error': str(e)})
#     finally:
#         # Close the cursor and connection
#         if cursor:
#             cursor.close()
#         if conn:
#             conn.close()

from flask import jsonify


@modelReport_blueprint.route("/model-report", methods=["GET"])
def model_report():
    conn = None
    cursor = None
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Retrieve distinct make, model, and year combinations
        cursor.execute("SELECT DISTINCT make, model, year FROM makes")
        make_model_year_combinations = cursor.fetchall()

        # Initialize list to store model reports
        model_reports = []

        # Iterate over each make, model, and year combination
        for make_model_year in make_model_year_combinations:
            make = make_model_year['make']
            model = make_model_year['model']
            years = make_model_year['year'].split(',')

            # Iterate over each year for the current make and model
            for year in years:
                # Query to get the average prices sorted by date in descending order
                cursor.execute("""
                    SELECT min_price,max_price,avg_price FROM price_sentiment 
                    WHERE make = %s AND model = %s AND year = %s
                    ORDER BY date DESC LIMIT 2
                """, (make, model, year))
                results = cursor.fetchall()

                # Check if there are at least two results
                if len(results) >= 2:
                    avg_price_last_day = results[0]['avg_price']
                    avg_price_before_last_day = results[1]['avg_price']
                    min_price = results[0]['min_price']
                    max_price = results[0]['max_price']

                    # Calculate the percentage difference
                    percentage_difference = 0
                    if avg_price_before_last_day != 0:
                        percentage_difference = ((
                                                             avg_price_last_day - avg_price_before_last_day) / avg_price_before_last_day) * 100

                    # Append the result to the model reports
                    model_report = {
                        'make': make,
                        'model': model,
                        'year': year,
                        'min_price': min_price,
                        'max_price': max_price,
                        'avg_price_before_last_day': avg_price_before_last_day,
                        'avg_price_last_day': avg_price_last_day,
                        'percentage_difference': percentage_difference
                    }
                    model_reports.append(model_report)

        # Return the model reports as JSON response
        return jsonify(model_reports)
    except Exception as e:
        # Return error message if an exception occurs
        return jsonify({'error': str(e)})
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()
