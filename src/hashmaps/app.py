from flask import Flask

from .models.cache import DEFAULT_CACHE_SIZE, QueueCache

__CACHE__ = QueueCache(DEFAULT_CACHE_SIZE)

app = Flask(__name__)
