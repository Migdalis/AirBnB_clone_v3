#!/usr/bin/python3
"""
Route to return a JSON about API status
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """Return a JSON with the API status"""
    data = {"status": "OK"}
    return jsonify(data)
