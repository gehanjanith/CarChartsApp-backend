from flask import Flask

from .DataService.routes_dropdowns import makes_blueprint, models_blueprint, year_blueprint
from .routes_MISreports import userReport_blueprint, searchRecordsReport_blueprint, vehicleListingsCountReport_blueprint
from .routes_appraisals import appraisalRequest_blueprint, getAllAppraisals_blueprint, valuationResponse_blueprint, \
    appraisalPerUser_blueprint, getAllNewAppraisals_blueprint
from .routes_comments import comments_blueprint, getComments_blueprint
from .routes_login import login_blueprint
from .routes_modelReport import modelReport_blueprint
from .routes_modelSearch import searchVehicle_blueprint
from .routes_plot import plot_blueprint
from .routes_privateMessages import savePrivateMessage_blueprint, getPrivateMessages_blueprint, \
    getUserPrivateMessages_blueprint, getPrivateMessagesPerAdvertisement_blueprint, \
    getAdvertisementPrivateMessagesPerUser_blueprint
from .routes_salePost import post_blueprint, getAllPosts_blueprint, getAllPostsPerUser_blueprint, deletePost_blueprint, \
    acceptOfferPost_blueprint
from .routes_search import search_blueprint
from .routes_sheduledJob import sheduledJob_blueprint
from .routes_users import addUser_blueprint, searchUser_blueprint, updateUser_blueprint, deleteUser_blueprint


def car_charts_app():
    app = Flask(__name__)
    app.register_blueprint(makes_blueprint)
    app.register_blueprint(models_blueprint)
    app.register_blueprint(year_blueprint)

    app.register_blueprint(plot_blueprint)

    app.register_blueprint(login_blueprint)

    app.register_blueprint(search_blueprint)

    app.register_blueprint(post_blueprint)
    app.register_blueprint(getAllPosts_blueprint)
    app.register_blueprint(getAllPostsPerUser_blueprint)
    app.register_blueprint(deletePost_blueprint)
    app.register_blueprint(acceptOfferPost_blueprint)

    app.register_blueprint(addUser_blueprint)
    app.register_blueprint(searchUser_blueprint)
    app.register_blueprint(updateUser_blueprint)
    app.register_blueprint(deleteUser_blueprint)

    app.register_blueprint(sheduledJob_blueprint)

    app.register_blueprint(userReport_blueprint)
    app.register_blueprint(searchRecordsReport_blueprint)
    app.register_blueprint(vehicleListingsCountReport_blueprint)

    app.register_blueprint(comments_blueprint)
    app.register_blueprint(getComments_blueprint)

    app.register_blueprint(savePrivateMessage_blueprint)
    app.register_blueprint(getPrivateMessages_blueprint)
    app.register_blueprint(getUserPrivateMessages_blueprint)
    app.register_blueprint(getPrivateMessagesPerAdvertisement_blueprint)
    app.register_blueprint(getAdvertisementPrivateMessagesPerUser_blueprint)

    app.register_blueprint(searchVehicle_blueprint)

    app.register_blueprint(modelReport_blueprint)

    app.register_blueprint(appraisalRequest_blueprint)
    app.register_blueprint(getAllAppraisals_blueprint)
    app.register_blueprint(getAllNewAppraisals_blueprint)
    app.register_blueprint(valuationResponse_blueprint)
    app.register_blueprint(appraisalPerUser_blueprint)

    return app
