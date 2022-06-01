#!/usr/bin/python3
"""
Route to return a JSON about API status
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """Return a JSON with the API status"""
    data = {"status": "OK"}
    return jsonify(data)


@app_views.route('/stats', strict_slashes=False)
def count_all():
    """Return a JSON that contains the number of each objects by type"""
    data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(data)
