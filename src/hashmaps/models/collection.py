from io import TextIOWrapper
from typing import Iterator, List, Tuple, Union

from .hashmap import HashMap


class Collection(HashMap):
    _map: List[List[Tuple[str, HashMap]]] = None

    def get(self, key: str, default: HashMap = None) -> Union[HashMap, None]:
        try:
            return self[key]

        except KeyError:
            if default:
                self[key] = default

            return default

    def pop(self, key: str) -> HashMap:
        return super().pop(key)

    def keys(self) -> Iterator[HashMap]:
        return super().keys()

    def items(self) -> Iterator[Tuple[str, HashMap]]:
        return super().items()

    def values(self) -> Iterator[HashMap]:
        return super().values()

    def load_from_file(self, file: TextIOWrapper) -> None:
        raise NotImplementedError("I haven't thought about this yet.")

    def to_csv(self, file: TextIOWrapper) -> None:
        raise NotImplementedError("I haven't thought about this yet.")

    def __getitem__(self, key: str) -> HashMap:
        return super().__getitem__(key)

    def __setitem__(self, key: str, value: HashMap) -> None:
        super().__setitem__(key, value)

    def __iter__(self) -> Iterator[HashMap]:
        return self.values()
