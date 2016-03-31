#!/usr/bin/env python

import os

from setuptools import setup, find_packages

from envy import VERSION

here = os.path.abspath(os.path.dirname(__file__))

required = [
    'future'
]

setup(
    name='envy',
    version=VERSION,
    packages=['envy'],
    url='https://github.com/shaunvxc/envy',
    license='MIT',
    author='Shaun Viguerie',
    author_email='shaunvig114@gmail.com',
    description='safely and easily debug files deep in python virtualenvs',
    entry_points={
        'console_scripts': ['envy = envy.application:main']
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'mock'],
    test_suite="tests",
    install_requires=required,
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: End Users/Desktop',
        'Topic :: System :: Shells',
        'Topic :: System :: System Shells',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
