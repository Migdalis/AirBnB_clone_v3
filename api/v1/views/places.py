#!/usr/bin/python3
"""
View for City objects that handles all default RESTFul API actions
"""
from os import abort
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """ Retrieves the list of all Place objects of a City """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = []
    for place in city.places:
        data.append(place.to_dict())
    return jsonify(data)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates a Place """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')


    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    user = storage.get(User, request.get_json()['user_id'])
    if not user:
        abort(404)

    if 'name' not in request.get_json():
        abort(400, 'Missing name')

    new_place = Place(**request.get_json())
    new_place.city_id = city_id
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a Place object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in request.get_json().items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
