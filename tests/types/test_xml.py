import pytest
from pydantic import BaseModel

from pyassorted.types._xml import to_xml_str


class TestToXmlStr:

    def test_basic_conversion(self):
        items = [
            {"id": 1, "name": "item1"},
            {"id": 2, "name": "item2"},
            {"id": 3, "name": "item3"},
        ]
        expected = '<items>\n<item id="1">item1</item>\n<item id="2">item2</item>\n<item id="3">item3</item>\n</items>'
        result = to_xml_str(items, attributes_keys=["id"], content_key="name")
        assert result == expected

    def test_custom_element_and_root_names(self):
        items = [{"value": "test"}]
        expected = "<root>\n<element>test</element>\n</root>"
        result = to_xml_str(
            items, content_key="value", element_name="element", root_name="root"
        )
        assert result == expected

    def test_with_pydantic_model(self):
        class Item(BaseModel):
            id: int
            name: str

        items = [Item(id=1, name="item1"), Item(id=2, name="item2")]
        expected = (
            '<items>\n<item id="1">item1</item>\n<item id="2">item2</item>\n</items>'
        )
        result = to_xml_str(items, attributes_keys=["id"], content_key="name")
        assert result == expected

    def test_with_indentation(self):
        items = [{"id": 1, "name": "item1"}]
        expected = '<items>\n  <item id="1">item1</item>\n</items>'
        result = to_xml_str(
            items, attributes_keys=["id"], content_key="name", indent="  "
        )
        assert result == expected

    def test_with_xml_declaration(self):
        items = [{"id": 1}]
        result = to_xml_str(items, attributes_keys=["id"], remove_xml_declaration=False)
        assert result.startswith("<?xml")

    def test_empty_list(self):
        items = []
        expected = "<items/>"
        result = to_xml_str(items)
        assert result == expected

    @pytest.mark.parametrize(
        "items, attributes_keys, content_key, expected",
        [
            ([{"a": 1, "b": 2}], ["a"], "b", '<items>\n<item a="1">2</item>\n</items>'),
            (
                [{"a": 1, "b": 2}],
                ["a", "b"],
                None,
                '<items>\n<item a="1" b="2"/>\n</items>',
            ),
            ([{"a": 1, "b": 2}], None, "b", "<items>\n<item>2</item>\n</items>"),
        ],
    )
    def test_various_attribute_and_content_combinations(
        self, items, attributes_keys, content_key, expected
    ):
        result = to_xml_str(
            items, attributes_keys=attributes_keys, content_key=content_key
        )
        assert result == expected
