#!/usr/bin/env python3
"""A script to Writing strings to Redis"""

import redis
import uuid
from functools import wraps
from typing import Union, Callable

def count_calls(method: Callable) -> Callable:
    """Decorator to count method calls"""

    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function for counting method calls"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper

def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs for a particular function"""

    key = method.__qualname__
    key_inputs = key + ":inputs"
    key_outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function for storing input and output history"""
        res = method(self, *args, **kwargs)
        self._redis.lpush(key_inputs, str(args))
        self._redis.rpush(key_outputs, str(res))
        return res

    return wrapper

class Cache:
    """A Cache class that stores data in Redis."""

    def __init__(self):
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis and return the key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float]:
        """Retrieve data from Redis and apply optional conversion function"""
        data = self._redis.get(key)
        if fn:
            return fn(data) if data else None
        else:
            return data

    def get_str(self, key: str) -> str:
        """Retrieve data from Redis as string"""
        return self.get(key, lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """Retrieve data from Redis as integer"""
        return self.get(key, lambda x: int(x))

    def replay(self, method: Callable):
        """Display the history of calls of a particular function"""
        key = method.__qualname__
        key_inputs = key + ":inputs"
        key_outputs = key + ":outputs"
        count = self.get(key).decode("utf-8")
        print(f"Cache.{key} was called {count} times:")
        inputs = self._redis.lrange(key_inputs, 0, -1)
        outputs = self._redis.lrange(key_outputs, 0, -1)
        zipped_list = list(zip(inputs, outputs))

        for i, (input, output) in enumerate(zipped_list):
            print(f"{key} (*{output}) -> {input}")

if __name__ == "__main__":
    cache = Cache()
    cache.store("first")
    cache.store("second")
    cache.store("third")
    cache.replay(cache.store)
