import builtins
import json
from dataclasses import is_dataclass
from typing import Any, get_origin, List, get_args, Union, Optional
from object_serializer.exceptions import InvalidDataTypeError

class Validator:
    """
    A utility class for validating dataclass types, JSON data, and type structures like lists and optionals.

    This class provides static methods to validate dataclass types, JSON strings, and more complex
    types such as lists and optionals. If a type is not valid, an InvalidDataTypeError is raised.
    """
    @staticmethod
    def validate_json(data: str) -> bool:
        """
        Validates if a given string is a valid JSON.

        This function attempts to parse a JSON string. If successful, it returns True.
        If the string cannot be parsed, it returns False.

        :param data: The string to be validated as JSON.
        :return: True if the string is valid JSON, False otherwise.
        :raises TypeError: If the data is None.
        """
        if data is None:
            raise TypeError('data must not be None')

        try:
            json.loads(data)
            return True
        except json.JSONDecodeError:
            return False

    # @staticmethod
    # def validate_datatype(cls: Any) -> bool:
    #     if is_dataclass(cls):
    #         return True
    #
    #     if cls in vars(builtins).values():
    #         return True
    #
    #     origin = get_origin(cls)
    #     if origin is list or origin is List:
    #         args = get_args(cls)
    #         if args:
    #             return Validator.validate_datatype(args[0])
    #         return True
    #
    #     if origin is Union and type(None) in get_args(cls):
    #         arg = [arg for arg in get_args(cls) if arg is not type(None)]
    #         if arg in vars(builtins).values() or arg is list or arg is List:
    #             return True
    #         else
    #
    #     raise NotADataclassError(cls)

    @staticmethod
    def validate_dataclass(cls: Any) -> bool:
        """
        Checks if a given object is a dataclass.

        This function uses the `is_dataclass` method to verify if the passed object is a valid dataclass.

        :param cls: The object to be checked.
        :return: True if the object is a dataclass, False otherwise.
        """
        return is_dataclass(cls)

    @staticmethod
    def validate_clslist(cls: Union[List[Any], list[Any]]) -> bool: # type: ignore
        """
        Validates if a given type is a valid list type.

        This function checks if the provided type is a list and validates its contents. It recursively
        verifies whether the inner type of the list is valid (primitives, lists, optionals, or dataclasses).

        :param cls: The type to be checked, which is expected to be a list.
        :return: True if the type is a valid list type.
        :raises InvalidDataTypeError: If the type is not a valid list or if the inner type is not valid.
        """
        if Validator.is_lst(cls):
            args = get_args(cls)
            if  not args:
                raise InvalidDataTypeError(cls, f"Class {cls} has none valid args")
            arg = args[0]
            if arg in vars(builtins).values():
                return True
            if Validator.is_lst(arg):
                return Validator.validate_clslist(arg)
            if Validator.is_optional(arg):
                return Validator.validate_clsoptional(arg)
            if Validator.validate_dataclass(arg):
                return True
            raise InvalidDataTypeError(arg, f"Class {arg} has not a valid datatype")
        raise InvalidDataTypeError(cls, f"Class {cls} is not a List class")

    @staticmethod
    def validate_clsoptional(cls: Optional[Any]) -> bool:
        """
        Validates if a given type is a valid Optional type.

        This function checks if the provided type is an Optional and validates its contents. It recursively
        verifies whether the inner type of the Optional is valid (primitives, lists, optionals, or dataclasses).

        :param cls: The type to be checked, which is expected to be an Optional.
        :return: True if the type is a valid Optional type.
        :raises InvalidDataTypeError: If the type is not a valid Optional or if the inner type is not valid.
        """
        if Validator.is_optional(cls):
            args = [arg for arg in get_args(cls) if arg is not type(None)]
            if not args:
                raise InvalidDataTypeError(cls, f"Class {cls} has none valid args")
            arg = args[0]
            if arg in vars(builtins).values():
                return True
            if Validator.is_lst(arg):
                return Validator.validate_clslist(arg)
            if Validator.is_optional(arg):
                return Validator.validate_clsoptional(arg)
            if Validator.validate_dataclass(arg):
                return True
            raise InvalidDataTypeError(arg, f"Class {arg} has not a valid datatype")
        raise InvalidDataTypeError(cls, f"Class {cls} is not a List class")

    @staticmethod
    def is_lst(cls: Any) -> bool:
        """
        Checks if a given type is a List.

        This function checks if the provided type has an origin of List or list.

        :param cls: The type to be checked.
        :return: True if the type is a List, False otherwise.
        """
        origin = get_origin(cls)
        return origin is List or origin is list

    @staticmethod
    def is_optional(cls: Any) -> bool:
        """
        Checks if a given type is an Optional.

        This function checks if the provided type has an origin of Union and contains a None type,
        indicating it is an Optional.

        :param cls: The type to be checked.
        :return: True if the type is an Optional, False otherwise.
        """
        origin = get_origin(cls)
        return origin is Union and type(None) in get_args(cls)
