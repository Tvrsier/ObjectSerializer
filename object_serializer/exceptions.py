from typing import Any


class NotADataclassError(Exception):
    def __init__(self, cls: Any):
        self.cls = cls
        super().__init__(f"The class {cls.__name__} is not a dataclass.")


class NotAJsonError(Exception):
    def __init__(self, json: str):
        self.json = json
        super().__init__(f"The provided JSON string is not valid: {json}")