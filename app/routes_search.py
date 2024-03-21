from flask import Blueprint, jsonify, request
from WebScrapingModule.scraper import scrape_riyasewana, scrape_ikman
from DatabaseModule.database import get_db_connection
from datetime import datetime
import mysql.connector

search_blueprint = Blueprint('scrape', __name__)


@search_blueprint.route("/scrape/<make>/<model>", methods=["GET"])
def scrape_both(make, model):
    args = request.args
    minYear = args.get('minYear')
    maxYear = args.get('maxYear')

    riyasewana_results = scrape_riyasewana(make, model, minYear, maxYear)
    ikman_results = scrape_ikman(make, model, minYear, maxYear)

    combined_results = riyasewana_results + ikman_results[1:]
    create_search_record(make, model, minYear, maxYear)

    out = {'results': [dict(zip(combined_results[0], row)) for row in combined_results[1:]]}
    return jsonify(out)


def create_search_record(make, model, minYear, maxYear):
    try:
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        # Create a new record in the 'search_records' table
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT INTO search_records (make, model, minYear, maxYear, timestamp) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (make, model, minYear, maxYear, timestamp))
        db_connection.commit()

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()
        db_connection.close()
