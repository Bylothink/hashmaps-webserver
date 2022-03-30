from .cache import QueueCache
from .collection import Collection
from .hashmap import HashMap

DEFAULT_CACHE_SIZE: int = 8
DEFAULT_COLLECTION_SIZE: int = 16
DEFAULT_HASH_MAP_SIZE: int = 64

HASH_MAPS: QueueCache = QueueCache(DEFAULT_CACHE_SIZE)
