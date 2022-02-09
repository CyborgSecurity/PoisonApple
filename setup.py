#!/usr/bin/env python

import os
from setuptools import setup

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="poisonapple",
    packages=[
        "poisonapple",
        "poisonapple.auxiliary",
    ],
    package_data={"poisonapple.auxiliary": ["*.plist", "*.sh"]},
    version="0.2.3",
    description="Command-line tool to perform various persistence mechanism techniques on macOS.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/CyborgSecurity/PoisonApple",
    author="Austin Jackson",
    author_email="vesche@protonmail.com",
    entry_points={
        "console_scripts": [
            "poisonapple = poisonapple.cli:main",
        ]
    },
    install_requires=[
        "crayons",
        "launchd",
        "python-crontab",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Topic :: Security",
    ],
)
