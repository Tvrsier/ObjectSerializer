<h1 align="center" id="title">ObjectSerializer</h1>

<p id="description">The object serializer is a python library designed to facilitate the conversion of JSON data into Python dataclasses. It provides utilities to validate JSON data against a given dataclass and automatically generate instances of the dataclass ensuring type safety and consinstency.</p>

<p align="center"><img src="https://img.shields.io/badge/python-3.7%7C3.8%7C3.9%7C3.10%7C3.11%7C3.12-blue" alt="shields"></p>

  
  
<h2>🧐 Features</h2>

Here are some of the project's best features:

*   JSON Validation: Validates that the structure and types of a given JSON match the expected dataclass structure
*   Automatic Dataclass Instantiation: Converts validated JSON data into instances of Python dataclasses.
*   Support for Nested and Optional Types: Handles nested dataclasses and optional types seamlessly

<h2>🛠️ Installation Steps:</h2>

<p>1. To install the Object Serializer clone this repository and install the dependencies:</p>

```bash
git clone https://github.com/Tvrsier/Object-Serializer.git 
cd object-serializer 
pip install -r requirements.txt
```

<h2>🚀 Usage:</h2>

```python
from dataclasses import dataclass
from object_serializer.serializer.json_parser import Parser

@dataclass
class InnerObject:
    born_in: str
    city_cap: int

@dataclass
class NestedObject:
    name: str
    age: int
    active: bool
    info: InnerObject

json_data = {
    'name': 'John Doe',
    'age': 30,
    'active': True,
    'info': {
        'born_in': 'New York',
        'city_cap': 1001
    }
}

result = Parser.validate_and_parse(NestedObject, json_data)
print(result)
```

<h2>🍰 Contribution Guidelines:</h2>

Contributions are welcome! If you'd like to contribute please fork the repository and submit a pull request.

<h2>🛡️ License:</h2>

This project is licensed under the MIT License