import abc
import re
from functools import wraps
from typing import re as tre, Optional


class Cache:
    def __init__(self):
        self._regex = {}

    def __getattribute__(self, item):
        original = super().__getattribute__(item)
        if item.startswith("_"):
            return original

        @wraps(original)
        def do(*args):
            return self._cache(original, *args)
        return do

    def _cache(self, method, *args):
        key = tuple(args)
        if key not in self._regex:
            self._regex[key] = method(*args)
        return self._regex[key]

    # The cache method only needs to implement/return
    # the creation of an cached item, the cache itself
    # is handled by the __dunder__ method

    def regex_compile(self, pattern: str, flags: re.RegexFlag = 0) -> tre.Pattern:
        return re.compile(pattern, flags)


class StepController(abc.ABC):
    def __init__(self):
        self.cache: Optional[Cache] = None


class StatefulStepController(StepController):
    def __start__(self):
        pass

    def __finish__(self):
        pass


def step(func):
    return func
