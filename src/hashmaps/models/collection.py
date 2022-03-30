import csv

from io import StringIO
from typing import Iterator, List, Tuple, Union

from .hashmap import DEFAULT_HASH_MAP_SIZE, HashMap

DEFAULT_COLLECTION_SIZE: int = 16


class Collection(HashMap):
    # pylint: disable=useless-super-delegation

    _map: List[List[Tuple[str, HashMap]]] = None

    def get(self, key: str, default: HashMap = None) -> Union[HashMap, None]:
        try:
            return self[key]

        except KeyError:
            if default is not None:
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

    def from_csv(self, csv_string: str) -> None:
        str_io: StringIO = StringIO(csv_string)

        reader = csv.reader(str_io)
        for name, key, value in reader:
            hash_map = self.get(name, HashMap(DEFAULT_HASH_MAP_SIZE))

            if key != '':
                hash_map[key] = value

    def to_csv(self) -> None:
        str_io: StringIO = StringIO()

        writer = csv.writer(str_io)
        for name, hash_map in self.items():
            if not hash_map:
                writer.writerow([name, None, None])

                continue

            for key, value in hash_map.items():
                writer.writerow([name, key, value])

        return str_io.getvalue()

    def __getitem__(self, key: str) -> HashMap:
        return super().__getitem__(key)

    def __setitem__(self, key: str, value: HashMap) -> None:
        super().__setitem__(key, value)

    def __iter__(self) -> Iterator[HashMap]:
        return self.values()
