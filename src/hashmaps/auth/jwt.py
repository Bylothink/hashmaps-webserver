import os

from typing import Any, Callable, Dict

import jwt

from flask import Response, request
from jwt.exceptions import InvalidTokenError
from werkzeug.exceptions import Unauthorized

from ..response import ErrorDetail, json_response
from .context import Context

RouteFunct = Callable[[Any, Any], Response]
AuthRouteFunct = Callable[[Context, Any, Any], Response]

try:
    JWT_SECRET = os.environ['SECRET_KEY']

except KeyError as exc:
    raise RuntimeError("SECRET_KEY environment variable is not set") from exc


def authenticate(funct: AuthRouteFunct) -> RouteFunct:
    def _funct_wrapper(*args, **kwargs) -> Response:
        # pylint: disable=redefined-outer-name

        auth_token: str = request.headers.get('Authorization')
        if not auth_token:
            error_code = 'empty_token'
            error_message = "You must be authenticated to perform this action"

            response = json_response(error=ErrorDetail(error_code, error_message), status_code=401)

            raise Unauthorized(error_message, response)

        try:
            payload: Dict[str, Any] = jwt.decode(auth_token, JWT_SECRET, ['HS256'])

        except InvalidTokenError as exc:
            error_code = 'invalid_token'
            error_message = "The token you're using is invalid"

            response = json_response(error=ErrorDetail(error_code, error_message), status_code=401)

            raise Unauthorized(error_message, response) from exc

        return funct(Context(payload), *args, **kwargs)

    # SMELLS: This fix a problem that Flask has with decorated routes.
    #         See https://stackoverflow.com/questions/17256602/
    _funct_wrapper.__name__ = funct.__name__

    return _funct_wrapper
