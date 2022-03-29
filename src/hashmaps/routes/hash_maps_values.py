from flask import Response, abort, jsonify, request
from typing import Dict

from ..app import app
from ..models import HASH_MAPS


@app.route("/<name>/<key>", methods=['POST'])
def create_hash_map_value(name: str, key: str) -> Response:
    value: str = request.get_data(as_text=True)
    if name not in HASH_MAPS:
        abort(404)

    hash_map: Dict[str, str] = HASH_MAPS[name]
    if key in hash_map:
        abort(409)

    hash_map[key] = value

    return jsonify(True)

@app.route("/<name>/<key>", methods=['GET'])
def read_hash_map_value(name: str, key: str) -> Response:
    if name not in HASH_MAPS:
        abort(404)

    hash_map: Dict[str, str] = HASH_MAPS[name]
    if key not in hash_map:
        abort(404)

    return jsonify(hash_map[key])

@app.route("/<name>/<key>", methods=['PUT'])
def update_hash_map_value(name: str, key: str) -> Response:
    value: str = request.get_data(as_text=True)
    if name not in HASH_MAPS:
        abort(404)

    hash_map: Dict[str, str] = HASH_MAPS[name]
    if key not in hash_map:
        abort(404)

    hash_map[key] = value

    return jsonify(True)

@app.route("/<name>/<key>", methods=['DELETE'])
def delete_hash_map_value(name: str, key: str) -> Response:
    if name not in HASH_MAPS:
        abort(404)

    hash_map: Dict[str, str] = HASH_MAPS[name]
    if key not in hash_map:
        abort(404)

    del hash_map[key]

    return jsonify(True)
