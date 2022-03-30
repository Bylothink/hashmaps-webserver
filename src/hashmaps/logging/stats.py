import logging

from os import path
from typing import Any, Callable

from flask import Response, request
from werkzeug.exceptions import HTTPException

from ..auth.context import Context

AuthRouteFunct = Callable[[Context, Any, Any], Response]

LOGS_PATH: str = '.volume/logs'


_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)

formatter = logging.Formatter('[%(asctime)s] %(message)s.')

file_handler = logging.FileHandler(path.join(LOGS_PATH, 'stats.log'))
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

_logger.addHandler(file_handler)


def log(funct: AuthRouteFunct) -> AuthRouteFunct:
    def _log(info: Context, status_code: int) -> None:
        _logger.info("Status code: %s  - User: %s - Resource: '%s' - Action: '%s'",
            status_code,
            repr(info.username),
            request.path,
            request.method
        )

    def _funct_wrapper(info: Context, *args, **kwargs) -> Response:
        try:
            response = funct(info, *args, **kwargs)

            _log(info, response.status_code)

            return response

        except HTTPException as exc:
            if exc.response:
                status_code = exc.response.status_code

            else:
                status_code = exc.code

            _log(info, status_code)

            raise

    # SMELLS: This fix a problem that Flask has with decorated routes.
    #         See https://stackoverflow.com/questions/17256602/
    _funct_wrapper.__name__ = funct.__name__

    return _funct_wrapper
