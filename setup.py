#!/usr/bin/env python

import os
from setuptools import setup

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='poisonapple',
    packages=['poisonapple'],
    version='0.1.1',
    description='Command-line tool to perform various persistence mechanism techniques on macOS.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/CyborgSecurity/PoisonApple',
    author='Austin Jackson',
    author_email='austin@cyborgsecurity.com',
    entry_points={
        'console_scripts': [
            'poisonapple = poisonapple.cli:main',
        ]
    },
    install_requires=[
        'crayons',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Topic :: Security'
    ]
)