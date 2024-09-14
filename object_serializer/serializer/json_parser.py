from typing import Any, Optional, List, Dict, get_args, get_origin

from dataclass_serializer import serialize
from object_serializer.exceptions import TypeValueMismatchError, InvalidDataTypeError
from validations import Validator


class Parser:
    @staticmethod
    def validate_types(cls_dict: Dict[str, Any], data: Dict[str, Any]) -> bool:
        for key, value in cls_dict.items():
            is_optional = Validator.is_optional(value)
            is_list = Validator.is_lst(value)
            if is_optional:
                if not Parser.validate_optional_type(value, data.get(key)):
                    raise TypeValueMismatchError(key, value, type(data.get(key)),
                                                 f"Expected type {value}, but either"
                                                 f"it's not None or"
                                                 f"{[arg for arg in get_args(value) if arg is not None][0]}")

            elif is_list:
                if not Parser.validate_list_type(value, data.get(key)):
                    raise TypeValueMismatchError(key, value, type(data.get(key)),
                                                 f"Expected array of type {value}, but either it's not or "
                                                 f"not all values of it are {[arg for arg in get_args(value)][0]}")

            elif Validator.validate_dataclass(value):
                if isinstance(data.get(key), Dict):
                    new_obj = data.get(key)
                    value_dict = serialize(value)
                    Parser.validate_types(value_dict, new_obj)
                else:
                    raise TypeValueMismatchError(key, value, type(data.get(key)),
                                                 f"Expected a new object, found {type(data.get(key)).__name__}"
                                                 f"instead")
            else:
                if not isinstance(data.get(key), value):
                    raise TypeValueMismatchError(key, value, type(data.get(key)),
                                                 f"Expected type {value}, found "
                                                 f"{type(data.get(key))} instead")
        return True

    @staticmethod
    def validate_list_type(expected: Any, actual: Any) -> bool:
        if not isinstance(actual, List):
            return False
        arg = get_args(expected)[0]
        if Validator.is_optional(arg):
            return Parser.validate_optional_type(arg, actual)
        elif Validator.is_lst(arg):
            return all(Parser.validate_list_type(arg, actual_value) for actual_value in actual)
        elif Validator.validate_dataclass(arg):
            serialized_cls = serialize(arg)
            return all(Parser.validate_types(serialized_cls, actual_value) for actual_value in actual)
        elif all(isinstance(value, arg) for value in actual):
            return True
        return False



    @staticmethod
    def validate_optional_type(expected: Any, actual: Any) -> bool:
        if actual is None:
            return True
        arg = [argv for argv in get_args(expected) if argv is not None][0]
        if Validator.is_optional(arg):
            raise InvalidDataTypeError(arg, "Optional cannot contain Optional")
        elif Validator.is_lst(arg):
            return Parser.validate_list_type(arg, actual)
        elif Validator.validate_dataclass(arg) and Validator.is_dict(type(actual)):
            return Parser.validate_types(serialize(arg), actual)
        elif isinstance(actual, arg):
            return True
        else:
            return False
