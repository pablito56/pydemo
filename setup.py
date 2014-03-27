#-*- coding: utf-8 -*-
u"""pydemo setup.py packaging and distribution script
"""
from setuptools import setup, find_packages
from itertools import imap
import platform
import os


def _replace_readline(req):
    if req.startswith("readline"):
        return "pyreadline"
    return req


def get_requirements(replace_readline=False):
    reqs_file = 'requirements_win.txt' if platform.system().lower() == "windows" else 'requirements.txt'
    try:
        with open(reqs_file) as reqs_file:
            reqs = filter(None, imap(lambda line: line.replace('\n', '').strip(), reqs_file))
            if replace_readline:
                reqs = map(_replace_readline, reqs)
            return reqs
    except IOError:
        pass
    return []

exceptions = []
for reqs in (get_requirements(), get_requirements(True)):
    try:
        setup(
            name="pydemo",
            version="0.0.7",
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
            install_requires=reqs,
            test_suite='nose.collector',
            tests_require="nose",
        )
        break
    except SystemExit, e:
        print "\n\tCaught SystemExit. Trying alternative requirements\n"
        exceptions.append(e)
else:
    print "\n\tScript failed. Caught to following SystemExit exceptions:"
    for e in exceptions:
        print e
