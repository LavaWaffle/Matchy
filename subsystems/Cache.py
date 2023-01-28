import time, json, os

CACHE_OUTDATED_SECONDS = 3600

class Cache:
    def __init__(self):
        if not os.path.exists("cache.json"):
            self.clear()
        else:
            with open("cache.json") as f:
                cache_json = json.load(f)
            self.__data = cache_json["data"]
            self.__times = cache_json["times"]

    def __setitem__(self, key, value):
        self.__data[key] = value
        self.__times[key] = time.time()

    def __getitem__(self, key):
        return self.__data.get(key)

    def is_outdated(self, key):
        return time.time() - self.__times.get(key, 0) >= CACHE_OUTDATED_SECONDS

    def clear(self):
        self.__data = {}
        self.__times = {}
        self.save()

    def save(self):
        with open("cache.json", "w") as f:
            json.dump({"data": self.__data, "times": self.__times}, f, indent = 4)