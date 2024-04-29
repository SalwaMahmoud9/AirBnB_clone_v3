#!/usr/bin/python3
"""Reviews"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/reviews/post_reviews.yml', methods=['POST'])
def post_review(place_id):
    """add review"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Wrong format")

    if 'user_id' not in request.get_json():
        abort(400, description="Please add user_id")

    data = request.get_json()
    user = storage.get(User, data['user_id'])

    if not user:
        abort(404)

    if 'text' not in request.get_json():
        abort(400, description="Please add text")

    data['place_id'] = place_id
    instance = Review(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/reviews/put_reviews.yml', methods=['PUT'])
def put_review(review_id):
    """update review"""
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    if not request.get_json():
        abort(400, description="Wrong format")

    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    data = request.get_json()
    for k, v in data.items():
        if k not in ignore:
            setattr(review, k, v)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/reviews/get_reviews.yml', methods=['GET'])
def get_reviews(place_id):
    """get review"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]

    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/reviews/get_review.yml', methods=['GET'])
def get_review(review_id):
    """get one review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/reviews/delete_reviews.yml', methods=['DELETE'])
def delete_review(review_id):
    """delete review"""

    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    storage.delete(review)
    storage.save()

    return make_response(jsonify({}), 200)