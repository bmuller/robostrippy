#!/usr/bin/env python
from setuptools import setup, find_packages

from robostrippy import version

setup(
    name="robostrippy",
    version=version,
    description="Strip HTML websites as though they provided a REST interface.  Like a Robot.",
    author="Brian Muller",
    author_email="bamuller@gmail.com",
    license="MIT",
    url="http://github.com/bmuller/robostrippy",
    packages=find_packages(),
    install_requires=["beautifulsoup4>=4.3.1", "requests>=1.2.3", "lxml>=3.2.3"]
)
