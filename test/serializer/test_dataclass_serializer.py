import unittest
from dataclasses import dataclass
from typing import List, Optional

from object_serializer.serializer import dataclass_serializer
from object_serializer.exceptions import InvalidDataTypeError
import pprint


class TestDataclassSerializer(unittest.TestCase):

    test_case_ids = {
        "test_simple_dataclass": "TCL_01",
        "test_simple_list": "TCL_02",
        "test_optional_class": "TCL_03",
        "test_optional_list": "TCL_04",
        "test_error_dataclass": "TCL_05",
        "test_error_no_arg_optional": "TCL_06",
        "test_error_no_arg_list": "TCL_07",
        "test_nested_dataclass": "TCL_08",
        "test_nested_optional_dataclass": "TCL_09",
        "test_optional_list_dataclass": "TCL_10"
    }

    def print_result(self, result, test_name):
        case_id = self.test_case_ids.get(test_name, "UNKNOWN")
        print(f"TEST {case_id} ({test_name}) RESULT:")
        pprint.pprint(result)
        print("\n")

    def test_simple_dataclass(self):
        @dataclass
        class SimpleDataClass:
            name: str
            age: int
            active: bool

        expected_result = {
            'name': str,
            'age': int,
            'active': bool
        }

        result = dataclass_serializer.serialize(SimpleDataClass)
        self.print_result(result, "test_simple_dataclass")
        self.assertEqual(result, expected_result)

    def test_simple_list(self):
        @dataclass
        class ListDataClass:
            name: str
            age: int
            active: bool
            results: List[int]

        expected_result = {
            'name': str,
            'age': int,
            'active': bool,
            'results': List[int]
        }

        result = dataclass_serializer.serialize(ListDataClass)
        self.print_result(result, "test_simple_list")
        self.assertEqual(result, expected_result)

    def test_optional_class(self):
        @dataclass
        class OptionalDataClass:
            name: str
            age: int
            active: bool
            sign: Optional[str]

        expected_result = {
            'name': str,
            'age': int,
            'active': bool,
            'sign': Optional[str]
        }
        result = dataclass_serializer.serialize(OptionalDataClass)
        self.print_result(result, "test_optional_class")
        self.assertEqual(result, expected_result)

    def test_optional_list(self):
        @dataclass
        class OptionalListClass:
            name: str
            age: int
            active: bool
            sign: Optional[List[int]]

        expected_result = {
            'name': str,
            'age': int,
            'active': bool,
            'sign': Optional[List[int]]
        }
        result = dataclass_serializer.serialize(OptionalListClass)
        self.print_result(result, "test_optional_list")
        self.assertEqual(result, expected_result)

    def test_error_dataclass(self):
        class NotDataclass:
            def __init__(self):
                self.name = "a"
        @dataclass
        class ErrorDataClass:
            name: str
            age: int
            active: bool
            sign: NotDataclass

        with self.assertRaises(InvalidDataTypeError):
            dataclass_serializer.serialize(ErrorDataClass)

    def test_error_no_arg_optional(self):
        @dataclass
        class ErrorDataClass:
            name: str
            age: int
            active: bool
            sign: Optional  # type: ignore

        with self.assertRaises(InvalidDataTypeError):
            dataclass_serializer.serialize(ErrorDataClass)

    def test_error_no_arg_list(self):
        @dataclass
        class ErrorDataClass:
            name: str
            age: int
            active: bool
            sign: List

        with self.assertRaises(InvalidDataTypeError):
            dataclass_serializer.serialize(ErrorDataClass)

    def test_nested_dataclass(self):
        @dataclass
        class InnerDataClass:
            lives_in: str
            born_in: str
            cap: int
            is_employeed: bool

        @dataclass
        class ComplexDataClass:
            name: str
            age: int
            active: bool
            info: InnerDataClass

        expected_result = {
            'name': str,
            'age': int,
            'active': bool,
            'info': InnerDataClass
        }

        result = dataclass_serializer.serialize(ComplexDataClass)
        self.print_result(result, "test_nested_dataclass")
        self.assertEqual(result, expected_result)

    def test_nested_optional_dataclass(self):
        @dataclass
        class InnerDataClass:
            lives_in: str
            born_in: str
            cap: int
            is_employeed: bool

        @dataclass
        class ComplexDataClass:
            name: str
            age: int
            active: bool
            info: Optional[InnerDataClass]

        expected_result = {
            'name': str,
            'age': int,
            'active': bool,
            'info': Optional[InnerDataClass]
        }

        result = dataclass_serializer.serialize(ComplexDataClass)
        self.print_result(result, "test_nested_optional_dataclass")
        self.assertEqual(result, expected_result)

    def test_optional_list_dataclass(self):
        @dataclass
        class InnerDataClass:
            lives_in: str
            born_in: str
            cap: int
            is_employeed: bool

        @dataclass
        class OptionalListClass:
            name: str
            age: int
            active: bool
            sign: Optional[List[InnerDataClass]]

        expected_result = {
            'name': str,
            'age': int,
            'active': bool,
            'sign': Optional[List[InnerDataClass]]
        }
        result = dataclass_serializer.serialize(OptionalListClass)
        self.print_result(result, "test_optional_list_dataclass")
        self.assertEqual(result, expected_result)
