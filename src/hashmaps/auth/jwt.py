from typing import Any, Callable, Dict

import jwt

from flask import Response, abort, request
from jwt.exceptions import InvalidTokenError

from .context import Context

RouteFunct = Callable[[Any, Any], Response]
AuthRouteFunct = Callable[[Context, Any, Any], Response]

JWT_SECRET = 'just-not-a-very-secure-secretkey'


def authenticate(funct: AuthRouteFunct) -> RouteFunct:
    def _funct_wrapper(*args, **kwargs) -> Response:
        auth_token: str = request.headers.get('Authorization')
        if not auth_token:
            abort(401)

        try:
            payload: Dict[str, Any] = jwt.decode(auth_token, JWT_SECRET, ['HS256'])

        except InvalidTokenError:
            abort(401)

        return funct(Context(payload), *args, **kwargs)

    # SMELLS: This fix a problem that Flask has with decorated routes.
    #         See https://stackoverflow.com/questions/17256602/
    _funct_wrapper.__name__ = funct.__name__

    return _funct_wrapper
