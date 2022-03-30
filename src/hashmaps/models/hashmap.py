import csv

from io import StringIO
from typing import Iterator, List, Tuple, Union

DEFAULT_HASH_MAP_SIZE: int = 64


class HashMap:
    _size: int = None

    _map: List[List[Tuple[str, str]]] = None
    _length: int = None

    @property
    def size(self) -> int:
        return self._size

    def __init__(self, size: int):
        if size < 1:
            raise ValueError("Size must be greater than 0")

        self._size = size
        self._initialize_map()

    def _initialize_map(self) -> None:
        self._map = [None] * self._size
        self._length = 0

    def get(self, key: str, default: str = None) -> Union[str, None]:
        try:
            return self[key]

        except KeyError:
            return default

    def pop(self, key: str) -> str:
        value = self[key]

        del self[key]

        return value

    def keys(self) -> Iterator[str]:
        for item in self.items():
            yield item[0]

    def items(self) -> Iterator[Tuple[str, str]]:
        for bucket in self._map:
            if bucket is not None:
                for item in bucket:
                    yield item

    def values(self) -> Iterator[str]:
        for item in self.items():
            yield item[1]

    def from_csv(self, csv_string: str) -> None:
        """
        Loads the key-value pairs from a CSV format string into the hash map.

        Example:
            >>> hash_map = HashMap(16)
            >>> hash_map.from_csv('a,1\\nb,2\\nc,3\\n')
            >>> hash_map
            HashMap(16): {'a': '1', 'b': '2', 'c': '3'}
            >>> hash_map.from_csv('d,4\\nb,5\\n')
            >>> hash_map
            HashMap(16): {'a': '1', 'b': '5', 'c': '3', 'd': '4'}
        """

        str_io: StringIO = StringIO(csv_string)

        reader = csv.reader(str_io)
        for key, value in reader:
            self[key] = value

    def to_csv(self) -> str:
        """
        Returns the key-value pairs from the hash map into a CSV format string.

        Example:
            >>> hash_map = HashMap(16)
            >>> hash_map['a'] = '1'
            >>> hash_map['b'] = '2'
            >>> hash_map['c'] = '3'
            >>> hash_map
            HashMap(16): {'a': '1', 'b': '2', 'c': '3'}
            >>> hash_map.to_csv()
            'a,1\\nb,2\\nc,3\\n'
        """

        str_io: StringIO = StringIO()

        writer = csv.writer(str_io)
        writer.writerows(self.items())

        return str_io.getvalue()

    def clear(self) -> None:
        self._initialize_map()

    def __getitem__(self, key: str) -> str:
        hashed_key: int = hash(key) % self._size
        bucket: List[Tuple[str, str]] = self._map[hashed_key]

        if bucket is None:
            raise KeyError(key)

        for item in bucket:
            if item[0] == key:
                return item[1]

        raise KeyError(key)

    def __setitem__(self, key: str, value: str) -> None:
        hashed_key: int = hash(key) % self._size
        bucket: List[Tuple[str, str]] = self._map[hashed_key]

        if bucket is None:
            self._map[hashed_key] = [(key, value)]
            self._length += 1

            return

        for index, item in enumerate(bucket):
            if item[0] == key:
                bucket[index] = (key, value)

                return

        bucket.append((key, value))
        self._length += 1

    def __delitem__(self, key: str) -> None:
        hashed_key: int = hash(key) % self._size
        bucket: List[Tuple[str, str]] = self._map[hashed_key]

        if bucket is None:
            raise KeyError(key)

        for index, item in enumerate(bucket):
            if item[0] == key:
                del bucket[index]
                self._length -= 1

                if len(bucket) == 0:
                    self._map[hashed_key] = None

                return

        raise KeyError(key)

    def __bool__(self) -> bool:
        return bool(self._length)

    def __len__(self) -> int:
        return self._length

    def __iter__(self) -> Iterator[str]:
        return self.values()

    def __contains__(self, key: str) -> bool:
        try:
            self[key]

        except KeyError:
            return False

        return True

    def __str__(self) -> str:
        values: List[str] = []

        for key, value in self.items():
            values.append(f"{repr(key)}: {repr(value)}")

        return f"{{{', '.join(values)}}}"

    def __repr__(self) -> str:
        return f"HashMap({self._size}): {self}"
