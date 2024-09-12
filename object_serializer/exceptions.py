from dataclasses import field
from typing import Any, Dict, Optional


class NotADataclassError(Exception):
    def __init__(self, cls: Any):
        self.cls = cls
        super().__init__(f"The class {cls.__name__} is not a dataclass.")


class NotAJsonError(Exception):
    def __init__(self, json: str):
        self.json = json
        super().__init__(f"The provided JSON string is not valid: {json}")


class InvalidDataTypeError(Exception):
    def __init__(self, cls: Any, msg: str):
        self.cls = cls
        super().__init__(msg)


class UnresolvedAttributeError(Exception):
    """
    An error that indicates that a MANDATORY FIELD is not found inside a json or dictionary
    """
    def __init__(self, cls: Optional[Any], data: Dict[str, Any], field_name, msg: str):
        self.cls = cls
        self.data = data
        self.field_name = field_name
        super().__init__(msg)

class TypeValueMismatchError(Exception):
    """
    An error that indicates when a json field and a serialized dataclass has a type value mismatch
    """
    def __init__(self, field_name: str, cls_type: Any, json_type: any, msg: str):
        self.field_name = field_name
        self.cls_type = cls_type
        self.json_type = json_type
        super().__init__(msg)