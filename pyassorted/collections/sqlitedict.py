import numbers
import pickle
import sqlite3
from typing import Any, Text, Union


PrimitiveType = Union[str, numbers.Number]


class SqliteDict(object):
    def __init__(
        self, sqlite_filepath: Text = ":memory:", tablename: Text = "cache", **kwargs
    ):
        self._sqlite_filepath = sqlite_filepath
        self._tablename = tablename
        self._conn = sqlite3.connect(self._sqlite_filepath)
        self._cursor = self._conn.cursor()
        self._cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self._tablename} (key TEXT PRIMARY KEY, value TEXT)"
        )
        self._conn.commit()

    def __len__(self) -> int:
        self._cursor.execute(f"SELECT COUNT(*) FROM {self._tablename}")
        return self._cursor.fetchone()[0]

    def __getitem__(self, key: PrimitiveType) -> Any:
        self.validate_key(key=key)
        self._cursor.execute(f"SELECT value FROM {self._tablename} WHERE key=?", (key,))
        fetch_result = self._cursor.fetchone()
        if fetch_result is None:
            raise KeyError(f"Key {key} not found")
        value_bytes = fetch_result[0]
        return pickle.loads(value_bytes)

    def __setitem__(self, key: PrimitiveType, value: Any):
        self.validate_key(key=key)
        value_bytes = pickle.dumps(value)
        self._cursor.execute(
            f"INSERT INTO {self._tablename} (key, value) VALUES (?, ?)",
            (key, value_bytes),
        )

    def get(self, key: PrimitiveType, default: Any = None) -> Any:
        self.validate_key(key=key)
        try:
            return self[key]
        except KeyError:
            return default

    def validate_key(self, key: Any, raise_error: bool = True) -> bool:
        if isinstance(key, (str, numbers.Number, None)):
            return True
        if raise_error:
            raise TypeError(f"Key must be a primitive type, got {type(key)}")
        return False
