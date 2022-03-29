from flask import Response, abort, jsonify, request

from ..app import app
from ..models import DEFAULT_HASH_MAP_SIZE, HASH_MAPS, HashMap


@app.route("/<name>", methods=['POST'])
def create_hashmap(name: str) -> Response:
    if name in HASH_MAPS:
        abort(409)

    HASH_MAPS[name] = HashMap(DEFAULT_HASH_MAP_SIZE)

    return jsonify(True)

@app.route("/<name>", methods=['GET'])
def read_hashmap(name: str) -> Response:
    if name not in HASH_MAPS:
        abort(404)

    return jsonify({key: value for key, value in HASH_MAPS[name].items()})

@app.route("/<name>", methods=['PUT'])
def rename_hashmap(name: str) -> Response:
    value: str = request.get_data(as_text=True)
    if name not in HASH_MAPS:
        abort(404)

    hash_map: HashMap = HASH_MAPS.pop(name)
    HASH_MAPS[value] = hash_map

    return jsonify(True)

@app.route("/<name>", methods=['DELETE'])
def delete_hashmap(name: str) -> Response:
    if name not in HASH_MAPS:
        abort(404)

    del HASH_MAPS[name]

    return jsonify(True)
