#!/usr/bin/python3
"""index"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.review import Review
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """number of objects"""
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]

    num_objs = {}
    for c in range(len(classes)):
        num_objs[names[c]] = storage.count(classes[c])

    return jsonify(num_objs)
