from flask import Response, request

from werkzeug.exceptions import NotFound, Conflict

from ..app import app
from ..auth import jwt, Context
from ..logging import stats
from ..manager import CollectionManager
from ..models import HashMap
from ..response import ErrorDetail, json_response


@app.route('/<name>/<key>', methods=['POST'])
@jwt.authenticate
@stats.log
def create_hashmap_value(info: Context, name: str, key: str) -> Response:
    with CollectionManager(info.username) as collection:
        value: str = request.get_data(as_text=True)
        if name not in collection:
            error_code = 'not_found'
            error_message = f"The hashmap '{name}' was not found in you collection"

            response = json_response(error=ErrorDetail(error_code, error_message), status_code=404)

            raise NotFound(error_message, response)

        hash_map: HashMap = collection[name]
        if key in hash_map:
            error_code = 'already_exists'
            error_message = f"The key '{key}' already exists in the hashmap '{name}'"

            response = json_response(error=ErrorDetail(error_code, error_message), status_code=409)

            raise Conflict(error_message, response)

        hash_map[key] = value

    return json_response({'success': True})

@app.route('/<name>/<key>', methods=['GET'])
@jwt.authenticate
@stats.log
def read_hashmap_value(info: Context, name: str, key: str) -> Response:
    collection = CollectionManager(info.username).get()
    if name not in collection:
        error_code = 'not_found'
        error_message = f"The hashmap '{name}' was not found in you collection"

        response = json_response(error=ErrorDetail(error_code, error_message), status_code=404)

        raise NotFound(error_message, response)

    hash_map: HashMap = collection[name]
    if key not in hash_map:
        error_code = 'not_found'
        error_message = f"The key '{key}' was not found in the hashmap '{name}'"

        response = json_response(error=ErrorDetail(error_code, error_message), status_code=404)

        raise NotFound(error_message, response)

    return json_response({'value': hash_map[key]})

@app.route('/<name>/<key>', methods=['PUT'])
@jwt.authenticate
@stats.log
def update_hashmap_value(info: Context, name: str, key: str) -> Response:
    with CollectionManager(info.username) as collection:
        value: str = request.get_data(as_text=True)
        if name not in collection:
            error_code = 'not_found'
            error_message = f"The hashmap '{name}' was not found in you collection"

            response = json_response(error=ErrorDetail(error_code, error_message), status_code=404)

            raise NotFound(error_message, response)

        hash_map: HashMap = collection[name]
        if key not in hash_map:
            error_code = 'not_found'
            error_message = f"The key '{key}' was not found in the hashmap '{name}'"

            response = json_response(error=ErrorDetail(error_code, error_message), status_code=404)

            raise NotFound(error_message, response)

        hash_map[key] = value

    return json_response({'success': True})

@app.route('/<name>/<key>', methods=['DELETE'])
@jwt.authenticate
@stats.log
def delete_hashmap_value(info: Context, name: str, key: str) -> Response:
    with CollectionManager(info.username) as collection:
        if name not in collection:
            error_code = 'not_found'
            error_message = f"The hashmap '{name}' was not found in you collection"

            response = json_response(error=ErrorDetail(error_code, error_message), status_code=404)

            raise NotFound(error_message, response)

        hash_map: HashMap = collection[name]
        if key not in hash_map:
            error_code = 'not_found'
            error_message = f"The key '{key}' was not found in the hashmap '{name}'"

            response = json_response(error=ErrorDetail(error_code, error_message), status_code=404)

            raise NotFound(error_message, response)

        del hash_map[key]

    return json_response({'success': True})
