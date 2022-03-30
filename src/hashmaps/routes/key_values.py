from flask import Response, abort, jsonify, request

from ..app import app
from ..auth import jwt, Context
from ..models import DEFAULT_COLLECTION_SIZE, HASH_MAPS, Collection, HashMap


@app.route('/<name>/<key>', methods=['POST'])
@jwt.authenticate
def create_hashmap_value(info: Context, name: str, key: str) -> Response:
    user_collection: Collection = HASH_MAPS.get(info.username, Collection(DEFAULT_COLLECTION_SIZE))

    value: str = request.get_data(as_text=True)
    if name not in user_collection:
        abort(404)

    hash_map: HashMap = user_collection[name]
    if key in hash_map:
        abort(409)

    hash_map[key] = value

    return jsonify(True)

@app.route('/<name>/<key>', methods=['GET'])
@jwt.authenticate
def read_hashmap_value(info: Context, name: str, key: str) -> Response:
    user_collection: Collection = HASH_MAPS.get(info.username, Collection(DEFAULT_COLLECTION_SIZE))

    if name not in user_collection:
        abort(404)

    hash_map: HashMap = user_collection[name]
    if key not in hash_map:
        abort(404)

    return jsonify(hash_map[key])

@app.route('/<name>/<key>', methods=['PUT'])
@jwt.authenticate
def update_hashmap_value(info: Context, name: str, key: str) -> Response:
    user_collection: Collection = HASH_MAPS.get(info.username, Collection(DEFAULT_COLLECTION_SIZE))

    value: str = request.get_data(as_text=True)
    if name not in user_collection:
        abort(404)

    hash_map: HashMap = user_collection[name]
    if key not in hash_map:
        abort(404)

    hash_map[key] = value

    return jsonify(True)

@app.route('/<name>/<key>', methods=['DELETE'])
@jwt.authenticate
def delete_hashmap_value(info: Context, name: str, key: str) -> Response:
    user_collection: Collection = HASH_MAPS.get(info.username, Collection(DEFAULT_COLLECTION_SIZE))

    if name not in user_collection:
        abort(404)

    hash_map: HashMap = user_collection[name]
    if key not in hash_map:
        abort(404)

    del hash_map[key]

    return jsonify(True)
