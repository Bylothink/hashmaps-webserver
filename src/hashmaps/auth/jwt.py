from typing import Any, Dict

import jwt

from flask import abort, request
from jwt.exceptions import InvalidTokenError

from .context import Context

JWT_SECRET = 'just-not-a-very-secure-secretkey'


def authenticate(funct):
    def wrapper(*args, **kwargs):
        auth_token: str = request.headers.get('Authorization')
        if not auth_token:
            abort(401)

        try:
            payload: Dict[str, Any] = jwt.decode(auth_token, JWT_SECRET, ['HS256'])
            username: str = payload['username']

        except InvalidTokenError:
            abort(401)

        info: Context = Context(payload)

        return funct(info, *args, **kwargs)

    return wrapper
