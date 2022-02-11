"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# GET 
@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    return jsonify(members), 200


# GET (by ID)
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"El miembro no existe"}), 400


# POST
@app.route('/member', methods=['POST'])
def add_member():
    member = request.json

    if not member:
        return jsonify({"Necesario un miembro valido"}), 400
    jackson_family.add_member(member)
    return jsonify({"Miembro agregado con éxito"}), 200


# DELETE
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = jackson_family.delete_member(member_id)
    if not member:
        return jsonify({"El ID no existe"})
    print("Miembro eliminado")
    return jsonify(member)


# UPDATE/PUT
@app.route('/member/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    member = request.json
    if not member:
        return jsonify({"Se necesita un miembro valido"}), 400
    jackson_family.update_member(member_id, member)
    return jsonify(member)

#####################################################
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
