from flask import Blueprint, jsonify, request
from WebScrapingModule.scraper import scrape_riyasewana, scrape_ikman, convert_to_days

plot_blueprint = Blueprint('plot', __name__)


@plot_blueprint.route("/plot/<make>/<model>", methods=["GET"])
def scrape_and_plot_route(make, model):
    args = request.args
    minYear = args.get('minYear')
    maxYear = args.get('maxYear')

    riyasewana_results = scrape_riyasewana(make, model, minYear, maxYear)
    ikman_results = scrape_ikman(make, model, minYear, maxYear)

    combined_results = riyasewana_results + ikman_results[1:]

    combined_results.sort(key=lambda x: (convert_to_days(x[5]),
                                         float(x[1].replace(',', '')) if x[1].replace(',', '').replace('.', '',
                                                                                                       1).isdigit() else float(
                                             'inf')))

    out = {'results': [dict(zip(combined_results[0], row)) for row in combined_results[1:]]}
    print(out)
    return jsonify(out)
