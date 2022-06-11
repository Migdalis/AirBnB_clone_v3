#!/usr/bin/python3
""" """
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
import os


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

API_HOST = os.getenv('HBNB_API_HOST', default='0.0.0.0')
API_PORT = os.getenv('HBNB_API_PORT', default='5000')


@app.teardown_appcontext
def close_storage(self):
    """Close current session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Handle error not found"""
    err_msg = {"error": "Not found"}
    return make_response(jsonify(err_msg), 404)


if __name__ == "__main__":
    app.run(host=API_HOST, port=API_PORT, threaded=True)
