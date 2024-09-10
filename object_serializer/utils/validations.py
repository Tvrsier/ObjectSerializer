import builtins
import json
from dataclasses import is_dataclass
from typing import Any, get_origin, List, get_args, Union
from object_serializer.exceptions import NotADataclassError


class Validator:
    @staticmethod
    def validate_json(data: str) -> bool:
        if data is None:
            raise TypeError('data must not be None')

        try:
            json.loads(data)
            return True
        except json.JSONDecodeError:
            return False

    @staticmethod
    def validate_dataclass(cls: Any) -> bool:
        if is_dataclass(cls):
            return True

        if cls in vars(builtins).values():
            return False

        origin = get_origin(cls)
        if origin is list or origin is List:
            args = get_args(cls)
            if args:
                return Validator.validate_dataclass(args[0])
            return False

        if origin is Union and type(None) in get_args(cls):
            args = [arg for arg in get_args(cls) if arg is not type(None)]
            return Validator.validate_dataclass(args[0])

        raise NotADataclassError(cls)
