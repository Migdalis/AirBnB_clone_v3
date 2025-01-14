#!/usr/bin/python3
"""
View for Review objects that handles all default RESTFul API actions
"""
from os import abort
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """ Retrieves the list of all Review objects of a Place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = []
    for review in place.reviews:
        data.append(review.to_dict())
    return jsonify(data)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ Retrieves a Review object """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a Review object """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Creates a Review """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')

    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    user = storage.get(User, request.get_json()['user_id'])
    if not user:
        abort(404)

    if 'text' not in request.get_json():
        abort(400, 'Missing text')

    new_review = Review(**request.get_json())
    new_review.place_id = place_id
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Updates a Review object """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in request.get_json().items():
        if key not in ignore_keys:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
