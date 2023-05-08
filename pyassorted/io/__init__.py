import glob
import json
from pathlib import Path
from typing import Dict, Generator, List, Text, Tuple, Union


def merge_data(
    obj_1: Union[Dict, List],
    obj_2: Union[Dict, List],
) -> Union[Dict, List]:
    if isinstance(obj_1, Dict) and isinstance(obj_2, Dict):
        for _k, _v in obj_2.items():
            if _k in obj_1:
                obj_1[_k] = merge_data(obj_1[_k], _v)
            else:
                obj_1[_k] = _v
    elif isinstance(obj_1, List) and isinstance(obj_2, List):
        obj_1.extend(obj_2)
    else:
        raise TypeError(f"Cannot merge {type(obj_1)} with {type(obj_2)}")


def read_json(filepath: Text) -> Union[Dict, List]:
    with open(filepath, "r") as f:
        return json.load(f)


def read_json_recursively(
    dirpath: Union[Path, Text]
) -> Generator[Tuple[Text, Union[Dict, List]], None, None]:
    dirpath = Path(dirpath)
    if dirpath.exists() and dirpath.is_file():
        yield read_json(dirpath)
        return
    for filepath in glob.iglob(f"{dirpath}/**/*.json", recursive=True):
        yield (filepath, read_json(filepath))
