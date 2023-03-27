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
        """Least Recently Used (LRU) cache implemented with collections.OrderedDict.

        Parameters
        ----------
        maxsize : int, optional
            Maximum size of the cache, by default 0
        init_cache : Optional[Union["LRU", Dict[KeyType, ValueType]]], optional
            Initial cache, by default None. If LRU, it will share the same cache.
        sentinel : Optional[Any], optional
            Sentinel value, by default None

        Raises
        ------
        ValueError
            If initiating cache is larger than maxsize.
        """

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
        """Check if cache is full.

        Returns
        -------
        bool
            True if cache is full, False otherwise.
        """

        return self.maxsize > 0 and len(self.cache) >= self.maxsize

    def get(self, key: KeyType) -> Union[ValueType, EmptyType]:
        """Get value from cache.

        Parameters
        ----------
        key : KeyType
            Key to get value from.

        Returns
        -------
        Union[ValueType, EmptyType]
            Value if key exists, otherwise sentinel.
        """

        value = self.cache.get(key, self.sentinel)

        with self.lock:
            if value is self.sentinel:
                self.misses += 1
                return self.sentinel
            else:
                self.hits += 1
                self.cache.move_to_end(key)
                return value

    def put(self, key: KeyType, value: ValueType):
        """Put value into cache.

        Parameters
        ----------
        key : KeyType
            Key to put value into.
        value : ValueType
            Value to put into cache.
        """

        if key in self.cache:
            with self.lock:
                self.cache.move_to_end(key)
                return

        with self.lock:
            self.cache[key] = value
            if self.maxsize > 0 and len(self.cache) > self.maxsize:
                self.cache.popitem(last=False)
