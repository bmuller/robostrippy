#!/usr/bin/env python
from setuptools import setup, find_packages
import robostrippy

setup(
    name="robostrippy",
    version=robostrippy.__version__,
    description="Strip HTML websites as though they provided a REST interface.  Like a Robot.",
    author="Brian Muller",
    author_email="bamuller@gmail.com",
    license="MIT",
    url="http://github.com/bmuller/robostrippy",
    packages=find_packages(),
    install_requires=["beautifulsoup4>=4.5.1", "requests>=2.11.0", "lxml>=3.6.1"]
)
