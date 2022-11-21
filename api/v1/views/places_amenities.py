#!/usr/bin/python3
"""Contain functions that handle views for the link between Place
objects and Amenity objects
"""

import os
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<string:place_id>/amenities',
                 methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """get amenity information for a specified place"""
    pl_obj = storage.get("Place", place_id)
    if not pl_obj:
        abort(404)
    amenities = []
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        am_objs = pl_obj.amenities
    else:
        am_objs = pl_obj.amenity_ids
    for amenity in am_objs:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """deletes an amenity object from a place"""
    pl_obj = storage.get("Place", place_id)
    am_obj = storage.get("Amenity", amenity_id)
    if not pl_obj or not am_obj:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        pl_am = pl_obj.amenities
    else:
        pl_am = pl_obj.amenity_ids
    if amenity not in pl_am:
        abort(404)
    pl_am.remove(amenity)
    pl.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """adds an amenity object to a place"""
    pl_obj = storage.get("Place", place_id)
    am_obj = storage.get("Amenity", amenity_id)
    if not pl_obj or not am_obj:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        pl_am = pl_obj.amenities
    else:
        pl_am = pl_obj.amenity_ids
    if am_obj in pl_am:
        return jsonify(am_obj.to_dict())
    pl_am.append(am_obj)
    pl_obj.save()
    return make_response(jsonify(am_obj.to_dict()), 201)
