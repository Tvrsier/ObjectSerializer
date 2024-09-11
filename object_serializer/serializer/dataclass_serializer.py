import builtins
from typing import Any, Dict
from object_serializer.utils.validations import Validator
from dataclasses import fields
from object_serializer.exceptions import InvalidDataTypeError


def serialize(cls: Any) -> Dict[str, Any]:
    """
    Serializes a dataclass into a dictionary that maps field names to their types.

    This function inspects the fields of a given dataclass and maps each field's name
    to its respective type. It supports the following types: primitive types (builtins),
    lists (List), optionals (Optional), and other dataclasses (dataclass).

    If a field's type is not valid (not a dataclass, list, or optional), an
    InvalidDataTypeError is raised.

    :param cls: The dataclass to be serialized.
    :param args: args
    :return: A dictionary where the keys are field names and the values are their respective types.
    :raises InvalidDataTypeError: If a field's type is neither a dataclass, a primitive type,
                                 nor a valid data structure.
    """
    cls_dict = {}
    for field in fields(cls):
        field_type = field.type

        if Validator.validate_dataclass(field_type):
            cls_dict[field.name] = field_type
        elif field_type in vars(builtins).values():
            cls_dict[field.name] = field_type
        else:
            if Validator.is_lst(field_type):
                if Validator.validate_clslist(field_type):
                    cls_dict[field.name] = field_type
            elif Validator.is_optional(field_type):
                if Validator.validate_clsoptional(field_type):
                    cls_dict[field.name] = field_type
            else:
                raise InvalidDataTypeError(field_type, f"Field '{field.name}' with type {field_type} is not valid")

    return cls_dict
