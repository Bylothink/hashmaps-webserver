from flask import Flask
from flask_cors import CORS

from .models.cache import DEFAULT_CACHE_SIZE, QueueCache

__CACHE__ = QueueCache(DEFAULT_CACHE_SIZE)

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
