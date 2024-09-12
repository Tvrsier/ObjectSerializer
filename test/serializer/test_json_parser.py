import unittest
from dataclasses import dataclass
from typing import List

from dataclass_serializer import serialize
from object_serializer.serializer.json_parser import Parser

class MyTestCase(unittest.TestCase):
    test_case_ids = {
        "test_simple": "TCL_01",
        "test_simple_list": "TCL_02",
        "test_nested_list": "TCL_03"
    }

    def test_simple(self):
        @dataclass
        class SimpleDataClass:
            name: str
            age: int
            active: bool

        json_data = {
            'name': 'name',
            'age': 0,
            'active': True
        }

        cls_dict = serialize(SimpleDataClass)
        self.assertTrue(Parser.validate_types(cls_dict, json_data))

    def test_simple_list(self):
        @dataclass
        class ListDataClass:
            name: str
            age: int
            active: bool
            arr_int: List[int]
            arr_str: List[str]
            arr_float: List[float]
            arr_bool: List[bool]

        json_data = {
            'name': 'name',
            'age': 0,
            'active': True,
            'arr_int': [0, 1, 2],
            'arr_str': ['a', 'b', 'c'],
            'arr_float': [0.1, 0.2, 0.3],
            'arr_bool': [True, False, True]
        }

        cls_dict = serialize(ListDataClass)
        self.assertTrue(Parser.validate_types(cls_dict, json_data))

    def test_nested_list(self):
        @dataclass
        class NestedList:
            name: str
            age: int
            active: bool
            arr: List[List[int]]

        json_data = {
            'name': 'name',
            'age': 0,
            'active': True,
            'arr': [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
        }

        cls_dict = serialize(NestedList)
        self.assertTrue(Parser.validate_types(cls_dict, json_data))

