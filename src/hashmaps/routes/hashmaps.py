from flask import Response, request

from werkzeug.exceptions import BadRequest, NotFound, Conflict

from ..app import app
from ..auth import jwt, Context
from ..logging import stats
from ..manager import CollectionManager
from ..models import DEFAULT_HASH_MAP_SIZE, HashMap
from ..response import ErrorDetail, json_response


@app.route('/', methods=['GET'])
@jwt.authenticate
@stats.log
def read_all_hashmaps(info: Context) -> Response:
    collection = CollectionManager(info.username).get()

    return json_response(collection.to_dict())

@app.route('/<name>', methods=['POST'])
@jwt.authenticate
@stats.log
def create_hashmap(info: Context, name: str) -> Response:
    with CollectionManager(info.username) as collection:
        if name in collection:
            error_code = 'already_exists'
            error_message = f"The hashmap '{name}' already exists in you collection"

            response = json_response(error=ErrorDetail(error_code, error_message), status_code=409)

            raise Conflict(error_message, response)

        collection[name] = HashMap(DEFAULT_HASH_MAP_SIZE)

    return json_response({'success': True})

@app.route('/<name>', methods=['GET'])
@jwt.authenticate
@stats.log
def read_hashmap(info: Context, name: str) -> Response:
    collection = CollectionManager(info.username).get()
    if name not in collection:
        error_code = 'not_found'
        error_message = f"The hashmap '{name}' was not found in you collection"

        response = json_response(error=ErrorDetail(error_code, error_message), status_code=404)

        raise NotFound(error_message, response)

    return json_response(collection[name].to_dict())

@app.route('/<name>', methods=['PUT'])
@jwt.authenticate
@stats.log
def rename_hashmap(info: Context, name: str) -> Response:
    with CollectionManager(info.username) as collection:
        if name not in collection:
            error_code = 'not_found'
            error_message = f"The hashmap '{name}' was not found in you collection"

            response = json_response(error=ErrorDetail(error_code, error_message), status_code=404)

            raise NotFound(error_message, response)

        value: str = request.get_data(as_text=True)
        if not value:
            error_code = 'empty_value'
            error_message = "The new hashmap name cannot be empty"

            response = json_response(error=ErrorDetail(error_code, error_message), status_code=400)

            raise BadRequest(error_message, response)

        hash_map: HashMap = collection.pop(name)
        collection[value] = hash_map

    return json_response({'success': True})

@app.route('/<name>', methods=['DELETE'])
@jwt.authenticate
@stats.log
def delete_hashmap(info: Context, name: str) -> Response:
    with CollectionManager(info.username) as collection:
        if name not in collection:
            error_code = 'not_found'
            error_message = f"The hashmap '{name}' was not found in you collection"

            response = json_response(error=ErrorDetail(error_code, error_message), status_code=404)

            raise NotFound(error_message, response)

        del collection[name]

    return json_response({'success': True})
