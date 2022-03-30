from flask import Response, abort, jsonify, request

from ..app import app
from ..auth import jwt, Context
from ..models import DEFAULT_COLLECTION_SIZE, DEFAULT_HASH_MAP_SIZE, HASH_MAPS, Collection, HashMap


@app.route('/<name>', methods=['POST'])
@jwt.authenticate
def create_hashmap(info: Context, name: str) -> Response:
    user_collection: Collection = HASH_MAPS.get(info.username, Collection(DEFAULT_COLLECTION_SIZE))

    if name in user_collection:
        abort(409)

    user_collection[name] = HashMap(DEFAULT_HASH_MAP_SIZE)

    return jsonify(True)

@app.route('/<name>', methods=['GET'])
@jwt.authenticate
def read_hashmap(info: Context, name: str) -> Response:
    user_collection: Collection = HASH_MAPS.get(info.username, Collection(DEFAULT_COLLECTION_SIZE))

    if name not in user_collection:
        abort(404)

    return jsonify(dict(user_collection[name].items()))

@app.route('/<name>', methods=['PUT'])
@jwt.authenticate
def rename_hashmap(info: Context, name: str) -> Response:
    user_collection: Collection = HASH_MAPS.get(info.username, Collection(DEFAULT_COLLECTION_SIZE))

    if name not in user_collection:
        abort(404)

    value: str = request.get_data(as_text=True)
    if not value:
        abort(400)

    hash_map: HashMap = user_collection.pop(name)
    user_collection[value] = hash_map

    return jsonify(True)

@app.route('/<name>', methods=['DELETE'])
@jwt.authenticate
def delete_hashmap(info: Context, name: str) -> Response:
    user_collection: Collection = HASH_MAPS.get(info.username, Collection(DEFAULT_COLLECTION_SIZE))

    if name not in user_collection:
        abort(404)

    del user_collection[name]

    return jsonify(True)
