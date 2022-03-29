from flask import Response, abort, jsonify, request
from typing import Dict

from ..app import app
from ..models import HASH_MAPS


@app.route("/<name>", methods=['POST'])
def create_hash_map(name: str) -> Response:
    if name in HASH_MAPS:
        abort(409)

    HASH_MAPS[name] = { }

    return jsonify(True)

@app.route("/<name>", methods=['GET'])
def read_hash_map(name: str) -> Response:
    if name not in HASH_MAPS:
        abort(404)

    return jsonify(HASH_MAPS[name])

@app.route("/<name>", methods=['PUT'])
def rename_hash_map(name: str) -> Response:
    value: str = request.get_data(as_text=True)
    if name not in HASH_MAPS:
        abort(404)

    hash_map: Dict[str, str] = HASH_MAPS.pop(name)
    HASH_MAPS[value] = hash_map

    return jsonify(True)

@app.route("/<name>", methods=['DELETE'])
def delete_hash_map(name: str) -> Response:
    if name not in HASH_MAPS:
        abort(404)

    del HASH_MAPS[name]

    return jsonify(True)
