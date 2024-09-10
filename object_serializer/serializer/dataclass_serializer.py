from typing import Any, Dict, List, get_origin, get_args, Union

from object_serializer.exceptions import NotADataclassError
from object_serializer.utils.validations import Validator
from dataclasses import fields
import builtins


def serialize(cls: Any) -> Dict[str, Any]:
    if not Validator.validate_dataclass(cls):
        raise NotADataclassError(cls)

    cls_dict = {}
    cls_origin = get_origin(cls)
    cls_args = get_args(cls)
    if cls_origin and (cls_origin is list or cls_origin is List):
        cls = cls_args[0]
    elif cls_origin and (cls_origin is Union and type(None) in cls_args):
        cls = [arg for arg in cls_args if arg is not type(None)][0]
    for field in fields(cls):
        field_type = field.type

        if Validator.validate_dataclass(field_type):
            cls_dict[field.name] = serialize(field_type)
        else:
            origin = get_origin(field_type)
            args = get_args(field_type)

            if origin is list or origin is List:
                cls_dict[field.name] = f"List[{args[0].__name__ if not Validator.validate_dataclass(args[0]) else
                serialize(args[0])}]"
            elif origin is Union and type(None) in args:
                non_none_type = [arg for arg in args if arg is not type(None)][0]
                cls_dict[field.name] = f"Optional[{non_none_type.__name__ if not
                Validator.validate_dataclass(non_none_type) else serialize(non_none_type)}]"
            else:
                cls_dict[field.name] = field_type.__name__

    return cls_dict
