from os import path

from .app import __CACHE__
from .models.collection import DEFAULT_COLLECTION_SIZE, Collection

COLLECTIONS_PATH: str = '.volume/collections'
DEFAULT_ENCODING: str = 'utf-8'


class CollectionManager:
    _username: str = None

    _collection: Collection = None

    @property
    def username(self) -> str:
        return self._username

    def __init__(self, username):
        self._username = username

    def get(self) -> Collection:
        try:
            self._collection = __CACHE__[self._username]

        except KeyError:
            self.load()

        return self._collection

    def load(self) -> Collection:
        self._collection = Collection(DEFAULT_COLLECTION_SIZE)
        filepath = path.join(COLLECTIONS_PATH, f'{self._username}.csv')
        if path.isfile(filepath):
            with open(filepath, mode='r', encoding=DEFAULT_ENCODING) as file:
                self._collection.from_csv(file.read())

        __CACHE__[self._username] = self._collection

        return self._collection

    def save(self) -> None:
        if self._collection is None:
            raise RuntimeError("Collection was not loaded properly")

        filepath = path.join(COLLECTIONS_PATH, f'{self._username}.csv')
        with open(filepath, mode='w', encoding=DEFAULT_ENCODING) as file:
            file.write(self._collection.to_csv())

    def __enter__(self) -> Collection:
        return self.get()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is None:
            self.save()
