#!/usr/bin/env python
# coding: utf-8
"""Project setup."""
import os
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

# This tool is as unopinionated as possible. There should be no requirements imposed by it.
REQUIREMENTS = []

TEST_REQUIREMENTS = [
    'pylama==7.1.0',
    'pytest==3.0.3',
]

setup(
    name='schaap',
    version='0.0.1',
    description='Probing profiler sending traces over the network to a schaapherder collector',
    long_description=README,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='profiler probing statistical schaapherder',
    author='Michał Pawłowski',
    author_email='@'.join(['unittestablecode', 'gmail.com']),
    license='MIT',
    py_modules=['schaap'],
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    extras_require={'tests': TEST_REQUIREMENTS},
)
