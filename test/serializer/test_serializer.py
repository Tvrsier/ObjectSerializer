import unittest
from dataclasses import dataclass
from typing import List, Optional, Any, Dict

from object_serializer.serializer import dataclass_serializer
from object_serializer.exceptions import NotADataclassError


class TestDataclassSerializer(unittest.TestCase):

    def test_simple_dataclass(self):
        @dataclass
        class SimpleDataClass:
            name: str
            age: int
            active: bool

        expected_result = {
            'name': 'str',
            'age': 'int',
            'active': 'bool'
        }

        result = dataclass_serializer.serialize(SimpleDataClass)
        self.assertEqual(result, expected_result)

    def test_simple_list(self):
        @dataclass
        class ListDataClass:
            name: str
            age: int
            active: bool
            results: List[int]

        expected_result = {
            'name': 'str',
            'age': 'int',
            'active': 'bool',
            'results': 'List[int]'
        }

        result = dataclass_serializer.serialize(ListDataClass)
        self.assertEqual(result, expected_result)

    def test_optional_class(self):
        @dataclass
        class OptionalDataClass:
            name: str
            age: int
            active: bool
            sign: Optional[str]

        expected_result = {
            'name': 'str',
            'age': 'int',
            'active': 'bool',
            'sign': 'Optional[str]'
        }
        result = dataclass_serializer.serialize(OptionalDataClass)
        self.assertEqual(result, expected_result)

    def test_optional_list(self):
        @dataclass
        class OptionalListClass:
            name: str
            age: int
            active: bool
            sign: Optional[List[int]]

        expected_result = {
            'name': 'str',
            'age': 'int',
            'active': 'bool',
            'sign': 'Optional[List]'
        }
        result = dataclass_serializer.serialize(OptionalListClass)
        self.assertEqual(result, expected_result)

    def test_error_class(self):
        class NotDataclass:
            def __init__(self):
                self.name = "a"
        @dataclass
        class ErrorDataClass:
            name: str
            age: int
            active: bool
            sign: NotDataclass

        with self.assertRaises(NotADataclassError):
            dataclass_serializer.serialize(ErrorDataClass)

    def test_nested_dataclass(self):
        @dataclass
        class InnerDataClass:
            lives_in: str
            born_in: str
            cap: int
            is_employeed: bool

            @staticmethod
            def __cls__dict__() -> Dict[str, Any]:
                return {
                    'lives_in': 'str',
                    'born_in': 'str',
                    'cap': 'int',
                    'is_employeed': 'bool'
                }

        @dataclass
        class ComplexDataClass:
            name: str
            age: int
            active: bool
            info: InnerDataClass

        expected_result = {
            'name': 'str',
            'age': 'int',
            'active': 'bool',
            'info': InnerDataClass.__cls__dict__()
        }

        result = dataclass_serializer.serialize(ComplexDataClass)
        self.assertEqual(result, expected_result)

    def test_nested_optional_dataclass(self):
        @dataclass
        class InnerDataClass:
            lives_in: str
            born_in: str
            cap: int
            is_employeed: bool

            @staticmethod
            def __cls__dict__() -> Dict[str, Any]:
                return {
                    'lives_in': 'str',
                    'born_in': 'str',
                    'cap': 'int',
                    'is_employeed': 'bool'
                }

        @dataclass
        class ComplexDataClass:
            name: str
            age: int
            active: bool
            info: Optional[InnerDataClass]

        expected_result = {
            'name': 'str',
            'age': 'int',
            'active': 'bool',
            'info': f'Optional[{InnerDataClass.__cls__dict__()}]'
        }

        result = dataclass_serializer.serialize(ComplexDataClass)
        self.assertEqual(result, expected_result)
