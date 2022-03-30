from flask import Response, abort, jsonify, request

from ..app import app
from ..auth import jwt, Context
from ..models import DEFAULT_HASH_MAP_SIZE, HASH_MAPS, HashMap


@app.route('/<name>', methods=['POST'])
@jwt.authenticate
def create_hashmap(info: Context, name: str) -> Response:
    if name in HASH_MAPS:
        abort(409)

    HASH_MAPS[name] = HashMap(DEFAULT_HASH_MAP_SIZE)

    return jsonify(True)

@app.route('/<name>', methods=['GET'])
@jwt.authenticate
def read_hashmap(info: Context, name: str) -> Response:
    if name not in HASH_MAPS:
        abort(404)

    return jsonify(dict(HASH_MAPS[name].items()))

@app.route('/<name>', methods=['PUT'])
@jwt.authenticate
def rename_hashmap(info: Context, name: str) -> Response:
    if name not in HASH_MAPS:
        abort(404)

    value: str = request.get_data(as_text=True)
    if not value:
        abort(400)

    hash_map: HashMap = HASH_MAPS.pop(name)
    HASH_MAPS[value] = hash_map

    return jsonify(True)

@app.route('/<name>', methods=['DELETE'])
@jwt.authenticate
def delete_hashmap(info: Context, name: str) -> Response:
    if name not in HASH_MAPS:
        abort(404)

    del HASH_MAPS[name]

    return jsonify(True)
