from flask import Response, abort, jsonify, request

from ..app import app
from ..auth import jwt, Context
from ..manager import CollectionManager
from ..models import HashMap


@app.route('/<name>/<key>', methods=['POST'])
@jwt.authenticate
def create_hashmap_value(info: Context, name: str, key: str) -> Response:
    with CollectionManager(info.username) as collection:
        value: str = request.get_data(as_text=True)
        if name not in collection:
            abort(404)

        hash_map: HashMap = collection[name]
        if key in hash_map:
            abort(409)

        hash_map[key] = value

    return jsonify(True)

@app.route('/<name>/<key>', methods=['GET'])
@jwt.authenticate
def read_hashmap_value(info: Context, name: str, key: str) -> Response:
    collection = CollectionManager(info.username).get()
    if name not in collection:
        abort(404)

    hash_map: HashMap = collection[name]
    if key not in hash_map:
        abort(404)

    return jsonify(hash_map[key])

@app.route('/<name>/<key>', methods=['PUT'])
@jwt.authenticate
def update_hashmap_value(info: Context, name: str, key: str) -> Response:
    with CollectionManager(info.username) as collection:
        value: str = request.get_data(as_text=True)
        if name not in collection:
            abort(404)

        hash_map: HashMap = collection[name]
        if key not in hash_map:
            abort(404)

        hash_map[key] = value

    return jsonify(True)

@app.route('/<name>/<key>', methods=['DELETE'])
@jwt.authenticate
def delete_hashmap_value(info: Context, name: str, key: str) -> Response:
    with CollectionManager(info.username) as collection:
        if name not in collection:
            abort(404)

        hash_map: HashMap = collection[name]
        if key not in hash_map:
            abort(404)

        del hash_map[key]

    return jsonify(True)
