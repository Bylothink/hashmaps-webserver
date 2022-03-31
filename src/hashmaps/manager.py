import os

from slugify import slugify

from .app import __CACHE__
from .models.collection import DEFAULT_COLLECTION_SIZE, Collection

DATA_VOLUME: str = os.environ.get('DATA_VOLUME', '.volume')
COLLECTIONS_PATH: str = f'{DATA_VOLUME}/collections'
DEFAULT_ENCODING: str = 'utf-8'


class CollectionManager:
    """
    `CollectionManager` allows you to persist collections
    consistently on disk while using a fast layer of caching.

    It use the `QueueCache` data structure.

    Each time a key is accessed, it attempts
    to retrieve the item from the cache.
    If it's not available, it tries to load it from the disk
    while also creating the relative key in the cache.

    Once an item has been modified, it saves it to the disk
    while also keeping it in the cache for quick future access.
    """

    _slug: str = None
    _collection: Collection = None

    def __init__(self, username):
        self._slug = slugify(username)

    def get(self) -> Collection:
        try:
            collection = __CACHE__[self._slug]

        except KeyError:
            collection = self.load()

        return collection

    def load(self) -> Collection:
        collection = Collection(DEFAULT_COLLECTION_SIZE)
        filepath = os.path.join(COLLECTIONS_PATH, f'{self._slug}.csv')
        if os.path.isfile(filepath):
            with open(filepath, mode='r', encoding=DEFAULT_ENCODING) as file:
                collection.from_csv(file.read())

        __CACHE__[self._slug] = collection

        return collection

    def save(self, collection: Collection) -> None:
        filepath = os.path.join(COLLECTIONS_PATH, f'{self._slug}.csv')
        with open(filepath, mode='w', encoding=DEFAULT_ENCODING) as file:
            file.write(collection.to_csv())

    def __enter__(self) -> Collection:
        self._collection = self.get()

        return self._collection

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is None:
            if self._collection is None:
                raise RuntimeError("Collection is not defined. Are you using nested `with` statements?")

            self.save(self._collection)

        self._collection = None
