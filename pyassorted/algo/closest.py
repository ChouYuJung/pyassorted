from typing import Any, Generic, List, Tuple, TypeVar

from typing_extensions import TypedDict

T = TypeVar("T")


class Entity(TypedDict, Generic[T]):
    start: int
    end: int
    value: T


def closest_entities(
    entities_1: List[Entity[T]], entities_2: List[Entity[T]]
) -> Tuple[List[T], List[T]]:
    items_1 = [item["value"] for item in entities_1]
    items_2 = [1] * len(items_1)  # Initialize with all ones

    for ent_2 in entities_2:
        closest_item_index = None
        closest_distance = float("inf")

        for idx, ent_1 in enumerate(entities_1):
            distance = abs(ent_1["start"] - ent_2["start"])
            if distance < closest_distance:
                closest_distance = distance
                closest_item_index = idx

        # If a closest item is found, update its corresponding number value
        if closest_item_index is not None:
            items_2[closest_item_index] = ent_2["value"]

    return items_1, items_2


if __name__ == "__main__":
    # Test
    items_entities = [
        {"start": 0, "end": 2, "value": "item_1"},
        {"start": 5, "end": 7, "value": "item_2"},
    ]
    numbers_entities = [{"start": 2, "end": 3, "value": 2}]
    print(closest_entities(items_entities, numbers_entities))

    items_entities = [
        {"start": 0, "end": 2, "value": "item_1"},
        {"start": 5, "end": 7, "value": "item_2"},
    ]
    numbers_entities = [{"start": 4, "end": 5, "value": 2}]
    print(closest_entities(items_entities, numbers_entities))

    items_entities = [
        {"start": 0, "end": 2, "value": "item_1"},
        {"start": 5, "end": 7, "value": "item_2"},
    ]
    numbers_entities = []
    print(closest_entities(items_entities, numbers_entities))
