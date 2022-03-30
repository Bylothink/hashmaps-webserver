from flask import Response, abort, jsonify, request

from ..app import app
from ..auth import jwt, Context
from ..logging import stats
from ..manager import CollectionManager
from ..models import DEFAULT_HASH_MAP_SIZE, HashMap


@app.route('/<name>', methods=['POST'])
@jwt.authenticate
@stats.log
def create_hashmap(info: Context, name: str) -> Response:
    with CollectionManager(info.username) as collection:
        if name in collection:
            abort(409)

        collection[name] = HashMap(DEFAULT_HASH_MAP_SIZE)

    return jsonify(True)

@app.route('/<name>', methods=['GET'])
@jwt.authenticate
@stats.log
def read_hashmap(info: Context, name: str) -> Response:
    collection = CollectionManager(info.username).get()
    if name not in collection:
        abort(404)

    return jsonify(dict(collection[name].items()))

@app.route('/<name>', methods=['PUT'])
@jwt.authenticate
@stats.log
def rename_hashmap(info: Context, name: str) -> Response:
    with CollectionManager(info.username) as collection:
        if name not in collection:
            abort(404)

        value: str = request.get_data(as_text=True)
        if not value:
            abort(400)

        hash_map: HashMap = collection.pop(name)
        collection[value] = hash_map

    return jsonify(True)

@app.route('/<name>', methods=['DELETE'])
@jwt.authenticate
@stats.log
def delete_hashmap(info: Context, name: str) -> Response:
    with CollectionManager(info.username) as collection:
        if name not in collection:
            abort(404)

        del collection[name]

    return jsonify(True)
