import copy
import glob
import json
from pathlib import Path
from typing import Dict, Generator, List, Text, Tuple, Union


def merge_data(
    obj_1: Union[Dict, List],
    obj_2: Union[Dict, List],
    inplace: bool = False,
) -> Union[Dict, List]:
    out = obj_1
    if inplace is False:
        out = copy.deepcopy(obj_1)
        obj_2 = copy.deepcopy(obj_2)

    if isinstance(out, Dict) and isinstance(obj_2, Dict):
        for _k, _v in obj_2.items():
            if _k in out:
                out[_k] = merge_data(out[_k], _v, inplace=inplace)
            else:
                out[_k] = _v

    elif isinstance(out, List) and isinstance(obj_2, List):
        out.extend(obj_2)

    else:
        raise TypeError(f"Cannot merge {type(obj_1)} with {type(obj_2)}")

    return out


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


def merge_json_recursively(dirpath: Union[Path, Text]) -> Union[Dict, List]:
    dirpath = Path(dirpath)

    obj = {}
    for _, _data in read_json_recursively(dirpath):
        obj = merge_data(obj, _data)
    return obj
