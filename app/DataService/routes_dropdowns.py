from flask import Blueprint, jsonify
from DatabaseModule.database import get_db_connection

makes_blueprint = Blueprint('makes', __name__)
models_blueprint = Blueprint('models', __name__)
year_blueprint = Blueprint('year', __name__)


@makes_blueprint.route("/makes", methods=["GET"])
def get_makes():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT make FROM makes")
        makes = [make[0] for make in cursor.fetchall()]
        return jsonify(makes)
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


@models_blueprint.route("/models/<make>", methods=["GET"])
def get_models(make):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT model FROM makes WHERE make = %s", (make,))
        models = [model[0] for model in cursor.fetchall()]
        return jsonify(models)
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


@year_blueprint.route("/year/<make>/<model>", methods=["GET"])
def get_models_year(make, model):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT year FROM makes WHERE make = %s AND model = %s", (make, model,))
        years_concatenated = cursor.fetchone()[0]  # Fetch the concatenated string of years
        years_list = years_concatenated.split(',')  # Split the string into individual years
        return jsonify(years_list)
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        cursor.close()
        conn.close()
