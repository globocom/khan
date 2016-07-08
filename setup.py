#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from khan import __version__, __author__, __email__

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [req[:-1] for req in open('requirements.txt', 'r').readlines()]

test_requirements = requirements

setup(
    name='khan-mongo',
    version=__version__,
    description="'hack day'",
    long_description=readme,
    author=__author__,
    author_email=__email__,
    url='https://github.com/otherpirate/khan',
    packages=[
        'khan',
    ],
    package_dir={'khan':
                 'khan'},
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'khan=khan.main:main',
        ],
    },
    license="MIT license",
    zip_safe=False,
    keywords='khan',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
