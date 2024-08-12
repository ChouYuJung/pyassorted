import hashlib
import importlib.machinery
import importlib.util
import sys
from typing import Callable, List, Optional, Set, Text

from typing_extensions import Required, TypedDict


class ModuleParam(TypedDict, total=False):
    module_name: Required[Text]  # Module name
    source_code: Required[Text]  # Source code
    md5: Optional[Text]  # MD5 hash


def _read_file(file_path: Text) -> Text:
    with open(file_path, "r") as file:
        return file.read()


def read_py_module(
    module_path: Text, excludes: Optional[Set[Text]] = None
) -> Optional[ModuleParam]:
    """Read the module source code."""

    if excludes is not None and module_path in excludes:
        return None

    # Load the module
    module = importlib.import_module(module_path)

    # Read the source code if it exists
    if (
        hasattr(module, "__file__")
        and module.__file__ is not None
        and module.__file__.endswith(".py")
    ):
        module_source_code = _read_file(module.__file__)
        return {
            "module_name": module.__name__,
            "source_code": module_source_code,
            "md5": hashlib.md5(module_source_code.encode()).hexdigest(),
        }

    return None


def read_module_with_dependencies(
    module_path: Text, filter: Optional[Callable[[Text], bool]] = None
) -> List[ModuleParam]:
    """Read the module source code."""

    modules: List[ModuleParam] = []
    walked_modules = set()

    # Parse the module path
    target_module_param = read_py_module(module_path)
    if target_module_param is not None:
        modules.append(target_module_param)
        walked_modules.add(module_path)
    else:
        raise ImportError(f"Module '{module_path}' not found.")

    # Read the dependencies
    for dep_name in sys.modules.keys():
        depend_module_param = read_py_module(dep_name, excludes=walked_modules)
        if depend_module_param is not None:
            modules.append(depend_module_param)
            walked_modules.add(dep_name)

    return modules
