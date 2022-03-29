import csv

from io import TextIOWrapper
from typing import Iterator, List, Tuple, Union


class HashMap:
    _size: int = None

    _map: List[List[Tuple[str, str]]] = None
    _length: int = None

    @property
    def size(self) -> int:
        return self._size

    def __init__(self, size: int):
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
            if bucket:
                for item in bucket:
                    yield item

    def values(self) -> Iterator[str]:
        for item in self.items():
            yield item[1]

    def load_from_file(self, file: TextIOWrapper) -> None:
        """
        Loads the key-value pairs from a CSV file into the hash map.

        Example:
            >>> hash_map = HashMap(16)
            >>> with open("dump.csv", "r") as file:
            >>>     hash_map.load_from_file(file)
        """

        reader = csv.reader(file)

        for key, value in reader:
            self[key] = value

    def dump_to_file(self, file: TextIOWrapper) -> None:
        """
        Dumps the key-value pairs from the hash map into a CSV file.

        Example:
            >>> hash_map = HashMap(16)
            >>> [...]
            >>> with open("dump.csv", "w") as file:
            >>>     hash_map.dump_to_file(file)
        """

        writer = csv.writer(file)

        for item in self.items():
            writer.writerow(item)

    def clear(self) -> None:
        self._initialize_map()

    def __getitem__(self, key: str) -> str:
        hashed_key: int = hash(key) % self._size
        bucket: List[Tuple[str, str]] = self._map[hashed_key]

        if not bucket:
            raise KeyError(key)

        for item in bucket:
            if item[0] == key:
                return item[1]

        raise KeyError(key)

    def __setitem__(self, key: str, value: str) -> None:
        hashed_key: int = hash(key) % self._size
        bucket: List[Tuple[str, str]] = self._map[hashed_key]

        if not bucket:
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

        if not bucket:
            raise KeyError(key)

        for index, item in enumerate(bucket):
            if item[0] == key:
                del bucket[index]
                self._length -= 1

                if not bucket:
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
        value: str = f"HashMap({self._size}):\n"

        for index, bucket in enumerate(self._map):
            if bucket:
                value += f"  {index}:\n"
                for item in bucket:
                    value += f"    {repr(item)}\n"

        return value
