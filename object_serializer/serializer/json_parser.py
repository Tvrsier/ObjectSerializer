import json
from typing import Any, List, Dict, get_args, Type, TypeVar, Union

from object_serializer.serializer.dataclass_serializer import serialize, gen_dataclass_instance
from object_serializer.exceptions import TypeValueMismatchError, InvalidDataTypeError
from object_serializer.utils.validations import Validator


T = TypeVar('T')


class Parser:
    @staticmethod
    def parse_json(data: str) -> Dict[str, Any]:
        """
        Converts a JSON string to a dictionary.

        :param data: The string to be parsed as JSON.
        :return: Parsed dictionary if valid JSON, otherwise raises JSONDecodeError.
        :raises TypeError: If the data is None.
        """
        if data is None:
            raise TypeError('data must not be None')

        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            raise e

    @staticmethod
    def validate_and_parse(cls: Type[T], data: Union[str, Dict[str, Any]]) -> T:
        """
        Validates a JSON string or dictionary against a dataclass and returns an instance of that dataclass.

        :param cls: The dataclass to validate against.
        :param data: JSON string or dictionary.
        :return: An instance of the dataclass.
        :raises TypeValueMismatchError: If any value in the JSON does not match the expected type.
        """

        if isinstance(data, str):
            data = Parser.parse_json(data)

        cls_dict = serialize(cls)
        validated_data = Parser._validate_types(cls, cls_dict, data)

        return validated_data

    @staticmethod
    def _validate_types(cls: Type[T], cls_dict: Dict[str, Any], data: Dict[str, Any]) -> T:
        """
        Validates the types of the JSON data against the dataclass and recursively constructs
        the dataclass instance.

        :param cls: The dataclass to validate against.
        :param cls_dict: The dictionary representation of the dataclass with expected types.
        :param data: The JSON data as a dictionary.
        :return: An instance of the dataclass populated with validated data.
        :raises TypeValueMismatchError: If any value in the JSON does not match the expected type.
        """
        validated_data = {}
        for key, value in cls_dict.items():
            is_optional = Validator.is_optional(value)
            is_list = Validator.is_lst(value)
            actual_value = data.get(key)

            if is_optional:
                validated_data[key] = Parser.validate_optional_type(key, value, actual_value)
            elif is_list:
                validated_data[key] = Parser.validate_list_type(key, value, actual_value)
            elif Validator.validate_dataclass(value):
                if isinstance(actual_value, Dict):
                    value_dict = serialize(value)
                    validated_data[key] = Parser._validate_types(value, value_dict, actual_value)
                else:
                    raise TypeValueMismatchError(key, value, type(actual_value),
                                                 f"Expected a new object at field {key},"
                                                 f" found {type(actual_value).__name__}"
                                                 f"instead")
            else:
                if not isinstance(actual_value, value):
                    if not ((value is int and isinstance(actual_value, float)) or
                            (value is float and isinstance(actual_value, int))):
                        raise TypeValueMismatchError(key, value, type(actual_value),
                                                     f"Expected type {value} at field {key}, found "
                                                     f"{type(actual_value)} instead")
                validated_data[key] = actual_value
        return gen_dataclass_instance(cls, validated_data)

    @staticmethod
    def validate_list_type(key: str, expected: Any, actual: Any) -> List[Any]:
        """
        Validates that a list matches the expected type.

        :param expected: The expected type of the list elements.
        :param actual: The actual list to validate.
        :param key: The field name that is being parsed
        :return: A list with validated elements.
        :raises TypeValueMismatchError: If the actual value is not a list or its elements do not match the expected type.
        """
        if not isinstance(actual, List):
            raise TypeValueMismatchError(
                key, expected, type(actual),
                f"Expected a list at field {key}, found {type(actual).__name__} instead"
            )
        arg = get_args(expected)[0]
        if Validator.is_optional(arg):
            return [Parser.validate_optional_type(key, arg, item) for item in actual]
        elif Validator.is_lst(arg):
            return [Parser.validate_list_type(key, arg, item) for item in actual]
        elif Validator.validate_dataclass(arg):
            return [Parser._validate_types(arg, serialize(arg), item) for item in actual]
        elif all(isinstance(value, arg) for value in actual):
            return actual
        else:
            raise TypeValueMismatchError(
                key, expected, type(actual),
                f"List items at field {key} do not match the expected type"
            )

    @staticmethod
    def validate_optional_type(key: str, expected: Any, actual: Any) -> Any:
        """
        Validates that an optional type matches the expected type or is None.

        :param expected: The expected optional type.
        :param actual: The actual value to validate.
        :param key: The field name that is being parsed
        :return: The validated value or None.
        :raises InvalidDataTypeError: If the expected type is an invalid Optional type.
        :raises TypeValueMismatchError: If the actual value does not match the expected type.
        """
        if actual is None:
            return None
        arg = [argv for argv in get_args(expected) if argv is not None][0]
        if Validator.is_optional(arg):
            raise InvalidDataTypeError(arg, "Optional cannot contain Optional")
        elif Validator.is_lst(arg):
            return Parser.validate_list_type(key, arg, actual)
        elif Validator.validate_dataclass(arg) and Validator.is_dict(type(actual)):
            return Parser._validate_types(arg, serialize(arg), actual)
        elif isinstance(actual, arg):
            return actual
        else:
            raise TypeValueMismatchError(
                "OptionalType", expected, type(actual),
                f"Expected type {arg} at field {key}, found {type(actual).__name__} instead"
            )
