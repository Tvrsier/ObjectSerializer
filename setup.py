from mypyc.doc.conf import author
from setuptools import setup, find_packages
setup(
    name="object-serializer",
    version="0.1.0",
    packages=find_packages(exclude=("test*", "examples*")),
    include_package_data=True,
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT License",
    author="Tvrsier"
)