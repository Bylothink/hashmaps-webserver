from typing import Iterator, List, Tuple, Union

from .collection import Collection

DEFAULT_CACHE_SIZE: int = 8


class QueueCache():
    """
    `QueueCache` is an implementation of a rotating
    cache that keeps in memory only the last `size` items.

    Each time a key is accessed, both for reading and writing,
    the item is moved to the first position in the list,
    shifting all the other items forward by one position.
    This keeps the most recently accessed items at the beginning
    of the list, making it faster to access them again.

    When the cache is full and you try to add a new item,
    the oldest accessed item is removed from the
    list leaving the place for the newer ones.

    For this reason, this data structure is not suitable
    for persistent storage, but it is very fast to access.
    """

    _size: int = None

    _queue: List[Tuple[str, Collection]] = None

    @property
    def size(self) -> int:
        return self._size

    def __init__(self, size: int):
        if size < 1:
            raise ValueError("Size must be greater than 0")

        self._size = size
        self._initialize_queue()

    def _initialize_queue(self) -> None:
        self._queue = []

    def get(self, key: str, default: Collection = None) -> Union[Collection, None]:
        try:
            return self[key]

        except KeyError:
            if default is not None:
                self[key] = default

            return default

    def pop(self, key: str) -> str:
        value = self[key]

        del self[key]

        return value

    def keys(self) -> Iterator[str]:
        for item in self.items():
            yield item[0]

    def items(self) -> Iterator[Tuple[str, Collection]]:
        for item in self._queue:
            yield item

    def values(self) -> Iterator[Collection]:
        for item in self.items():
            yield item[1]

    def clear(self) -> None:
        self._initialize_queue()

    def __getitem__(self, key: str) -> Collection:
        for index, item in enumerate(self._queue):
            if item[0] == key:
                del self._queue[index]
                self._queue.insert(0, item)

                return item[1]

        raise KeyError(key)

    def __setitem__(self, key: str, value: Collection) -> None:
        for index, item in enumerate(self._queue):
            if item[0] == key:
                del self._queue[index]
                self._queue.insert(0, (key, value))

                return

        self._queue.insert(0, (key, value))
        if len(self._queue) > self._size:
            self._queue.pop()

    def __delitem__(self, key: str) -> None:
        for index, item in enumerate(self._queue):
            if item[0] == key:
                del self._queue[index]

                return

        raise KeyError(key)

    def __bool__(self) -> bool:
        return bool(self._queue)

    def __len__(self) -> int:
        return len(self._queue)

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
        return f"QueueCache({self._size}): {self}"
