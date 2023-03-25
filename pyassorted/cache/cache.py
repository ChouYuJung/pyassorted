from collections import OrderedDict
from threading import RLock
from typing import Any, Dict, Optional, TypeVar, Union


KeyType = TypeVar("KeyType")
ValueType = TypeVar("ValueType")
EmptyType = TypeVar("EmptyType")

EMPTY_CACHE: EmptyType = object()


class LRU(object):
    def __init__(
        self,
        maxsize: int = 0,
        init_cache: Optional[Union["LRU", Dict[KeyType, ValueType]]] = None,
        sentinel: Optional[Any] = None,
    ):
        self.maxsize = 0 if maxsize < 0 else maxsize

        init_cache = OrderedDict() if init_cache is None else init_cache
        if self.maxsize > 0 and len(init_cache) > self.maxsize:
            raise ValueError("Initiating cache is larger than maxsize.")
        if isinstance(init_cache, LRU):
            self.cache: OrderedDict[KeyType, ValueType] = init_cache.cache
        else:
            self.cache = OrderedDict(init_cache)

        self.hits = 0
        self.misses = 0
        self.lock = RLock()
        self.sentinel = EMPTY_CACHE if sentinel is None else sentinel

    def __len__(self):
        return len(self.cache)

    def full(self) -> bool:
        return self.maxsize > 0 and len(self.cache) > self.maxsize

    def get(self, key: KeyType) -> Union[ValueType, EmptyType]:
        value = self.cache.get(key, self.sentinel)

        if value is self.sentinel:
            self.misses += 1
            return self.sentinel

        with self.lock:
            self.hits += 1
            self.cache.move_to_end(key)
            return value

    def put(self, key: KeyType, value: ValueType):
        if key in self.cache:
            with self.lock:
                self.cache.move_to_end(key)
                return

        with self.lock:
            self.cache[key] = value
            if self.full():
                self.cache.popitem(last=False)
