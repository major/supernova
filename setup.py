#!/usr/bin/python
#
# Copyright 2014 Major Hayden
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
from setuptools import setup


required_packages = [
    "click",
    "configobj",
    "importlib",
    "keyring<8.0",
    "python-novaclient",
    "six"
]

optional_packages = {
    'rackspace':  [
        'rackspace-novaclient'
    ]
}

setup(
    name='supernova',
    version='2.2.0',
    author='Major Hayden',
    author_email='major@mhtx.net',
    description="novaclient wrapper for multiple nova environments",
    install_requires=required_packages,
    extras_require=optional_packages,
    packages=['supernova'],
    url='https://github.com/major/supernova',
    entry_points='''
        [console_scripts]
        supernova = supernova.executable:run_supernova
        supernova-keyring = supernova.executable:run_supernova_keyring
    '''
    )
