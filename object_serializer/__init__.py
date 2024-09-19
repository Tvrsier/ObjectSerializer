from object_serializer.serializer.dataclass_serializer import serialize, gen_dataclass_instance
from object_serializer.serializer.json_parser import Parser
from object_serializer.exceptions import NotAJsonError, NotADataclassError
from object_serializer.utils.validations import Validator

VERSION = "0.1.0"

__all__ = [
    'Validator',
    'NotAJsonError',
    'NotADataclassError',
    'serialize',
    'gen_dataclass_instance',
    'Parser'
]