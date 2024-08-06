import importlib.machinery
import importlib.util
from typing import List, Text, TypedDict


class ModuleParam(TypedDict):
    module_name: Text  # Module name
    source_code: Text  # Source code


def _read_file(file_path: Text) -> Text:
    with open(file_path, "r") as file:
        return file.read()


def read_modules(module_path: Text) -> List[ModuleParam]:
    spec = importlib.util.find_spec(module_path)
    if spec is None:
        raise ImportError(f"Module '{module_path}' not found.")
    module = importlib.util.module_from_spec(spec)
    if module.__file__ is None:
        raise ImportError(f"Module '{module_path}' has no file.")

    source_code = _read_file(module.__file__)

    return [{"module_name": spec.name, "source_code": source_code}]
