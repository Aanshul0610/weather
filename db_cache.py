import json
import os
from datetime import datetime, timedelta

class DBCache:
    CACHE_FILE = "weather_cache.json"
    EXPIRY = timedelta(minutes=30)

    def __init__(self):
        if os.path.exists(self.CACHE_FILE):
            with open(self.CACHE_FILE, 'r') as f:
                self.cache = json.load(f)
        else:
            self.cache = {}

    def _is_expired(self, timestamp):
        then = datetime.fromisoformat(timestamp)
        return datetime.now() - then > self.EXPIRY

    def get(self, key):
        entry = self.cache.get(key)
        if entry and not self._is_expired(entry['ts']):
            return entry['data']
        return None

    def set(self, key, data):
        self.cache[key] = {
            'ts': datetime.now().isoformat(),
            'data': data
        }
        with open(self.CACHE_FILE, 'w') as f:
            json.dump(self.cache, f)
