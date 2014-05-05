#!/usr/bin/env python
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
import keyring


def password_get(username=None):
    """
    Retrieves a password from the keychain based on the environment and
    configuration parameter pair.
    """
    try:
        return keyring.get_password('supernova', username).encode('ascii')
    except:
        return False


def password_set(username=None, password=None):
    """
    Stores a password in a keychain for a particular environment and
    configuration parameter pair.
    """
    try:
        keyring.set_password('supernova', username, password)
        return True
    except:
        return False