import json

from typing import Any, Dict, List

from flask import Response


class ErrorDetail:
    _code: str = None
    _message: str = None

    @property
    def code(self) -> str:
        return self._code

    @property
    def message(self) -> str:
        return self._message

    def __init__(self, code: str, message: str) -> None:
        self._code: str = code
        self._message: str = message

    def to_dict(self) -> Dict[str, Any]:
        return {
            'code': self._code,
            'message': self._message
        }


def json_response(data: Dict[str, Any] = None,
                  error: ErrorDetail = None,
                  errors: List[ErrorDetail] = None,
                  status_code: int = 200) -> Response:

    json_obj = {
        'data': {},
        'errors': []
    }

    if data is not None:
        json_obj['data'] = data

    if errors is not None:
        json_obj['errors'] = [e.to_dict() for e in errors]

    elif error is not None:
        json_obj['errors'] = [error.to_dict()]

    return Response(json.dumps(json_obj),
                    status=status_code,
                    headers={'Access-Control-Allow-Origin': '*'},
                    mimetype="application/json")
