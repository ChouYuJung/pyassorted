import hashlib
import importlib.machinery
import importlib.util
from typing import List, Optional, Text

from typing_extensions import Required, TypedDict


class ModuleParam(TypedDict, total=False):
    module_name: Required[Text]  # Module name
    source_code: Required[Text]  # Source code
    md5: Optional[Text]  # MD5 hash


def _read_file(file_path: Text) -> Text:
    with open(file_path, "r") as file:
        return file.read()


def read_modules(module_path: Text) -> List[ModuleParam]:
    """Read the module source code."""

    spec = importlib.util.find_spec(module_path)
    if spec is None:
        raise ImportError(f"Module '{module_path}' not found.")
    module = importlib.util.module_from_spec(spec)
    if module.__file__ is None:
        raise ImportError(f"Module '{module_path}' has no file.")

    source_code = _read_file(module.__file__)
    md5 = hashlib.md5(source_code.encode()).hexdigest()

    return [{"module_name": spec.name, "source_code": source_code, "md5": md5}]
