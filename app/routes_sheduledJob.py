import mysql
import requests
from flask import Blueprint, jsonify, request
from bs4 import BeautifulSoup
from datetime import datetime

from DatabaseModule.database import db_config

sheduledJob_blueprint = Blueprint('price-scrape', __name__)


# price history analyse
def save_to_database(make, model, year, max_price, min_price, avg_price):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = "INSERT INTO price_sentiment (make, model, year, max_price, min_price, avg_price, date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (make, model, year, max_price, min_price, avg_price, current_date)
    cursor.execute(query, values)
    conn.commit()
    conn.close()


def scrape_price(make, model, minYear, maxYear):
    url = f"https://ikman.lk/en/ads/sri-lanka/cars/{make}/{model}?numeric.model_year.minimum={minYear}&numeric.model_year.maximum={maxYear}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    prices = []
    for link in soup.select('li[class*="normal-ad"]'):
        price_tag = link.select('div[class*="price"] span')[0].next
        # Preprocess the price string to remove non-numeric characters and convert it to a float
        price_numeric = float(''.join(filter(str.isdigit, price_tag)))
        prices.append(price_numeric)

    if prices:
        max_price = max(prices)
        min_price = min(prices)
        avg_price = sum(prices) / len(prices)
        return max_price, min_price, avg_price
    else:
        return None, None, None


@sheduledJob_blueprint.route("/price-scrape", methods=["GET"])
def scrape_data():
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for JSON output
        cursor.execute("SELECT make, model, year FROM makes")
        make_model_years = cursor.fetchall()

        for item in make_model_years:
            make = item['make']
            model = item['model']
            years_str = item['year']
            years = years_str.split(',')
            for year in years:
                max_price, min_price, avg_price = scrape_price(make, model, year,
                                                               year)  # Provide minYear and maxYear as year
                if max_price is not None:
                    save_to_database(make, model, year, max_price, min_price, avg_price)

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
