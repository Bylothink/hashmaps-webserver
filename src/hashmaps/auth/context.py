from typing import Any, Dict


class Context:
    _username: str = None

    @property
    def username(self) -> str:
        return self._username

    def __init__(self, payload: Dict[str, Any]):
        self._username = payload['username']
