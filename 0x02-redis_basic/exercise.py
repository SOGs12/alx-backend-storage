#!/usr/bin/env python3
"""A script to  Writing strings to Redis"""


import redis
import uuid
from functools import wraps
from typing import Union, Callable, Optional



def count_calls(method: Callable) -> Callable:
    """decorator takes a single method Callable
    argument and returns a Callable"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # get the function name from the wrapped function
        self._redis.incr(key)

        return method(self, *args, **kwargs)
    return wrapper



def call_history(method: Callable) -> Callable:
    """decorator to store the history of
    inputs and outputs for a particular function."""


    key = method.__qualname__
    key_inputs = key + ":inputs"
    key_outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """returns original method"""

        res = method(self, *args, **kwargs)
        self._redis.lpush(key_inputs, res)
        self._redis.rpush(key_outputs, str(args))

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
        """method that takes a data argument and returns a string"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key


    def get(self, key: str,
            fn: Callable = None) -> Union[str,
                                                    bytes, int, float]:
        """convert the data back to the desired format"""

        data = self._redis.get(key)
        if fn:
            return fn(data) if data else None
        else:
            return data

    def get_str(self, key: str):
        """automatically parametrize Cache.get
        with the correct conversion function"""
        return self._redis.get(key, lambda x: x.decode("utf-8"))


    def get_int(self, key: str):
        """automatically parametrize Cache.get
        with the correct conversion function"""
        return self.get(key, lambda x: int(x))


    def replay(self, method):
        """
        display the history of calls of a particular function

        """
        key = method.__qualname__
        key_inputs= key + ":inputs"
        key_outputs= key + ":outputs"
        # The count_calls decorator, when applied to
        # the store method, uses a separate key
        # derived from the method's qualified name
        # ("Cache.store" in this case) to keep
        # track of how many times the store method has been called.
        # This is a different key from the UUIDs used for storing data.
        count = self.get(key).decode("utf-8")
        print(f"Cache.{key} was called {count} times:")
        inputs = self._redis.lrange(key_inputs, 0, -1)
        outputs = self._redis.lrange(key_outputs, 0, -1)
        zipped_list = list(zip(inputs, outputs))

        for i, (input, output) in enumerate(zipped_list):
            print(f"{key} (*{output}) -> {input}")
