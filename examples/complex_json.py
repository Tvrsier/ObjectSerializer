from examples import fetch_data_from_api
from object_serializer.serializer.json_parser import Parser
from dataclasses import dataclass, asdict
from typing import List
import json

@dataclass
class Meta:
    createdAt: str
    updatedAt: str
    barcode: str
    qrCode: str



@dataclass
class Reviews:
    rating: int
    comment: str
    date: str
    reviewerName: str
    reviewerEmail: str



@dataclass
class Dimensions:
    width: float
    height: float
    depth: float


@dataclass
class Product:
    id: int
    title: str
    description: str
    category: str
    price: float
    discountPercentage: float
    rating: float
    stock: int
    tags: List[str]
    dimensions: Dimensions
    reviews: List[Reviews]
    meta: Meta
    availabilityStatus: str

@dataclass
class DummyJson:
    products: List[Product]


if __name__ == "__main__":
    api_url = "https://dummyjson.com/products"
    json_data = fetch_data_from_api(api_url)
    dummy = Parser.validate_and_parse(DummyJson, json_data)
    print(json.dumps(asdict(dummy), indent=4))
