import unittest
from dataclasses import dataclass
from typing import List, Optional

from object_serializer.exceptions import TypeValueMismatchError
from object_serializer.serializer.dataclass_serializer import serialize
from object_serializer.serializer.json_parser import Parser


class MyTestCase(unittest.TestCase):
    test_case_ids = {
        "test_simple": "TCL_01",
        "test_simple_list": "TCL_02",
        "test_nested_list": "TCL_03",
        "test_optional_list": "TCL_04",
        "test_nested_object": "TCL_05",
        "test_object_in_list": "TCL_06",
        "test_object_in_nested_list": "TCL_07",
        "test_object_in_optional_list": "TCL_08",
        "test_type_mismatch_error": "TCL_09",
        "test_type_mismatch_error_list": "TCL_10",
        "test_type_mismatch_error_nested_list": "TCL_11",
        "test_type_mismatch_in_optional": "TCL_12",
        "test_type_mismatch_in_nested_object": "TCL_13"
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

    def test_optional_list(self):
        @dataclass
        class OptionalList:
            name: str
            age: int
            active: bool
            arr: Optional[List[int]]

        json_data_1 = {
            'name': 'name',
            'age': 0,
            'active': True,
            'arr': [1, 2, 3]
        }

        json_data_2 = {
            'name': 'name',
            'age': 0,
            'active': True,
        }

        cls_dict = serialize(OptionalList)
        self.assertTrue(Parser.validate_types(cls_dict, json_data_1))
        self.assertTrue(Parser.validate_types(cls_dict, json_data_2))

    def test_nested_object(self):
        @dataclass
        class InnerList:
            born_in: str
            city_cap: int

        @dataclass
        class NestedObject:
            name: str
            age: int
            active: bool
            info: InnerList

        json_data = {
            'name': 'name',
            'age': 0,
            'active': True,
            'info': {
                'born_in': 'somewhere',
                'city_cap': 1001
            }
        }

        cls_dict = serialize(NestedObject)
        self.assertTrue(Parser.validate_types(cls_dict, json_data))

    def test_object_in_list(self):
        @dataclass
        class InnerList:
            born_in: str
            city_cap: int


        @dataclass
        class ObjectList:
            name: str
            age: int
            active: bool
            arr: List[InnerList]

        json_data = {
            'name': 'name',
            'age': 0,
            'active': True,
            'arr': [
                {
                    'born_in': 'somewhere',
                    'city_cap': 1001
                },
                {
                    'born_in': 'somewhere',
                    'city_cap': 1001
                },
                {
                    'born_in': 'somewhere',
                    'city_cap': 1001
                }
            ]
        }

        cls_dict = serialize(ObjectList)
        self.assertTrue(Parser.validate_types(cls_dict, json_data))

    def test_object_in_nested_list(self):
        @dataclass
        class InnerList:
            born_in: str
            city_cap: int


        @dataclass
        class ObjectList:
            name: str
            age: int
            active: bool
            arr: List[List[InnerList]]

        json_data = {
            'name': 'name',
            'age': 0,
            'active': True,
            'arr': [
                [
                    {
                        'born_in': 'somewhere',
                        'city_cap': 1001
                    },
                    {
                        'born_in': 'somewhere',
                        'city_cap': 1001
                    },
                    {
                        'born_in': 'somewhere',
                        'city_cap': 1001
                    }
                ],
                [
                    {
                        'born_in': 'somewhere',
                        'city_cap': 1001
                    },
                    {
                        'born_in': 'somewhere',
                        'city_cap': 1001
                    },
                    {
                        'born_in': 'somewhere',
                        'city_cap': 1001
                    }
                ],
                [
                    {
                        'born_in': 'somewhere',
                        'city_cap': 1001
                    },
                    {
                        'born_in': 'somewhere',
                        'city_cap': 1001
                    },
                    {
                        'born_in': 'somewhere',
                        'city_cap': 1001
                    }
                ]
            ]
        }

        cls_dict = serialize(ObjectList)
        self.assertTrue(Parser.validate_types(cls_dict, json_data))

    def test_object_in_optional_list(self):
        @dataclass
        class InnerList:
            born_in: str
            city_cap: int


        @dataclass
        class ObjectList:
            name: str
            age: int
            active: bool
            arr: Optional[List[InnerList]]

        json_data_1 = {
            'name': 'name',
            'age': 0,
            'active': True,
            'arr': [
                {
                    'born_in': 'somewhere',
                    'city_cap': 1001
                },
                {
                    'born_in': 'somewhere',
                    'city_cap': 1001
                },
                {
                    'born_in': 'somewhere',
                    'city_cap': 1001
                }
            ]
        }
        json_data_2 = {
            'name': 'name',
            'age': 0,
            'active': True,
        }

        cls_dict = serialize(ObjectList)
        self.assertTrue(Parser.validate_types(cls_dict, json_data_1))
        self.assertTrue(Parser.validate_types(cls_dict, json_data_2))

    def test_type_mismatch_error(self):
        @dataclass
        class SimpleDataClass:
            name: str
            age: int
            active: bool

        json_data = {
            'name': 'name',
            'age': 'abc',
            'active': True
        }

        cls_dict = serialize(SimpleDataClass)
        with self.assertRaises(TypeValueMismatchError):
            Parser.validate_types(cls_dict, json_data)

    def test_type_mismatch_error_list(self):
        @dataclass
        class SimpleDataClass:
            name: str
            age: int
            active: bool
            arr: List[int]

        json_data = {
            'name': 'name',
            'age': 0,
            'active': True,
            'arr': [
                1, 2, 'abc'
            ]
        }

        cls_dict = serialize(SimpleDataClass)
        with self.assertRaises(TypeValueMismatchError):
            Parser.validate_types(cls_dict, json_data)

    def test_type_mismatch_error_nested_list(self):
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
            'arr': [[1, 2, 3], [1, 2, 3], "abc"]
        }

        cls_dict = serialize(NestedList)
        with self.assertRaises(TypeValueMismatchError):
            Parser.validate_types(cls_dict, json_data)

    def test_type_mismatch_in_optional(self):
        @dataclass
        class OptionalClass:
            name: str
            age: int
            active: bool
            info: Optional[str]

        json_data = {
            'name': 'name',
            'age': 0,
            'active': True,
            'info': 1
        }

        cls_dict = serialize(OptionalClass)
        with self.assertRaises(TypeValueMismatchError):
            Parser.validate_types(cls_dict, json_data)

    def test_type_mismatch_in_nested_object(self):
        @dataclass
        class InnerList:
            born_in: str
            city_cap: int

        @dataclass
        class NestedObject:
            name: str
            age: int
            active: bool
            info: InnerList

        json_data = {
            'name': 'name',
            'age': 0,
            'active': True,
            'info': {
                'born_in': 10,
                'city_cap': 1001
            }
        }

        cls_dict = serialize(NestedObject)
        with self.assertRaises(TypeValueMismatchError):
            Parser.validate_types(cls_dict, json_data)