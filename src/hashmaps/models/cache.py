from typing import Iterator, List, Tuple, Union

from .collection import Collection


class QueueCache():
    _size: int = None

    _queue: List[Tuple[str, Collection]] = None

    @property
    def size(self) -> int:
        return self._size

    def __init__(self, size: int):
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

    def __str__(self) -> str:
        values: List[str] = []

        for key, value in self.items():
            values.append(f"{repr(key)}: {repr(value)}")

        return f"{{{', '.join(values)}}}"

    def __repr__(self) -> str:
        return f"QueueCache({self._size}): {self}"
