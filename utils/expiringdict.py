from collections.abc import Mapping
import time


class ExpiringDict(Mapping):
    def __init__(self, max_age_seconds, *args, **kwargs):
        self.max_age_seconds = max_age_seconds
        self._storage = dict(*args, **kwargs)

    def vacuum(self):
        vacuum_start = time.time()
        expired_keys = []
        for key, (value, create_time) in self._storage.items():
            if (create_time + self.max_age_seconds) < vacuum_start:
                expired_keys.append(key)

        for key in expired_keys:
            self._storage.pop(key)

    def __setitem__(self, key, value):
        create_time = time.time()
        self._storage.__setitem__(key, (value, create_time))

    def __getitem__(self, key):
        self.vacuum()
        (value, create_time) = self._storage.get(key, None)
        return value

    def __iter__(self):
        self.vacuum()
        return iter(self._storage)

    def __len__(self):
        self.vacuum()
        return len(self._storage)

    def __contains__(self, key):
        self.vacuum()
        return self._storage.__contains__(key)

    def __eq__(self, o):
        self.vacuum()
        return self._storage.__eq__(o)

    def __ne__(self, o):
        self.vacuum()
        return self._storage.__ne__(o)

    def keys(self):
        self.vacuum()
        return self._storage.keys()

    def items(self):
        self.vacuum()
        return self._storage.items()

    def values(self):
        self.vacuum()
        return self._storage.values()

    def get(self, key):
        return self.__getitem__(key)
