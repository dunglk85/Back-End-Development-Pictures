from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """return list of data"""
    if data:
        return jsonify(data), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """return picture by id"""
    for p in data:
        if p['id'] == id:
            return jsonify(p), 200

    return {"message": "Internal server error"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    # Extract picture data from the request body
    picture = request.get_json()

    # Check if the picture with the given id already exists
    for existing_picture in data:
        if existing_picture['id'] == picture['id']:
            # Picture with the given id already exists, return a 302 status code
            return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302

    # Add the picture data to the pictures list
    data.append(picture)

    # Return a success response
    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    # Extract picture data from the request body
    picture = request.get_json()

    # Check if the picture with the given id already exists
    for existing_picture in data:
        if existing_picture['id'] == picture['id']:
            # Update the existing picture data
            existing_picture.update(picture)
            return jsonify({"Message": "picture updated successfully"}), 200

    return jsonify({"Message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    # Check if the picture with the given id already exists
    for picture in data:
        if picture['id'] == id:
            data.remove(picture)
            return '', 204
    return jsonify({"Message": "picture not found"}), 404
