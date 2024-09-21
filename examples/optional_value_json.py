from examples import fetch_data_from_api
from object_serializer.serializer.json_parser import Parser
from dataclasses import dataclass, asdict
from typing import List, Optional
import json


@dataclass
class DummyJson:
    id: int
    title: str
    description: str
    category: str
    price: float
    discountPercentage: float
    rating: float
    stock: int
    sku: str
    availabilityStatus: str
    tags: Optional[List[str]]


if __name__ == "__main__":
    api_url = "https://dummyjson.com/c/c2f1-e092-4a73-b91e"
    json_data = fetch_data_from_api(api_url)
    dummy = Parser.validate_and_parse(DummyJson, json_data)
    print(json.dumps(asdict(dummy), indent=4))
