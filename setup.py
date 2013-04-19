#-*- coding: utf-8 -*-
u"""pydemo setup.py packaging and distribution script
"""
from setuptools import setup, find_packages
from itertools import imap
import platform
import os


def get_requirements():
    reqs_file = 'requirements_win.txt' if platform.system().lower() == "windows" else 'requirements.txt'
    try:
        with open(reqs_file) as reqs_file:
            reqs = filter(None, imap(lambda line: line.replace('\n', '').strip(), reqs_file))
            return reqs
    except IOError:
        pass
    return []


setup(
    name="pydemo",
    version="0.0.3",
    description="Python code demonstration console for didactic purposes",
    long_description="Python code demonstration console for didactic purposes. \
Prints and executes input files in blocks of lines. Extends code.InteractiveConsole",
    author="Pablo Enfedaque",
    author_email='pablito56@gmail.com',
    url="https://github.com/pablito56/pydemo",
    packages=find_packages(exclude=['test*']),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pydemo = pydemo.pydemo:main',
        ]
    },
    install_requires=get_requirements(),
    test_suite='nose.collector',
    tests_require="nose",
)
