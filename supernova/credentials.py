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
"""
Handles all of the interactions with the operating system's keyring
"""
from __future__ import print_function


import getpass
import re
import sys


import keyring


from . import colors
from . import utils


def get_user_password(env, param, force=False):
    """
    Allows the user to print the credential for a particular keyring entry
    to the screen
    """
    username = utils.assemble_username(env, param)

    if not utils.confirm_credential_display(force):
        return

    # Retrieve the credential from the keychain
    password = password_get(username)

    if password:
        return (username, password)
    else:
        return False


def pull_env_credential(env, param, value):
    """
    Dissects a keyring credential lookup string from the supernova config file
    and returns the username/password combo
    """
    rex = "USE_KEYRING\[([\x27\x22])(.*)\\1\]"

    # This is the old-style, per-environment keyring credential
    if value == "USE_KEYRING":
        username = utils.assemble_username(env, param)

    # This is the new-style, global keyring credential that can be applied
    # to multiple environments
    else:
        global_identifier = re.match(rex, value).group(2)
        username = utils.assemble_username('global', global_identifier)

    return (username, password_get(username))


def password_get(username=None):
    """
    Retrieves a password from the keychain based on the environment and
    configuration parameter pair.
    """
    return keyring.get_password('supernova', username).encode('ascii')


def set_user_password(args):
    """
    Sets a user's password in the keyring storage
    """
    print("""
[%s] Preparing to set a password in the keyring for:

  - Environment  : %s
  - Parameter    : %s

If this is correct, enter the corresponding credential to store in your keyring
or press CTRL-D to abort:""" % (colors.gwrap("Keyring operation"), args.env,
                                args.parameter))

    # Prompt for a password and catch a CTRL-D
    try:
        password = getpass.getpass('')
    except:
        password = None
        print()

    # Did we get a password from the prompt?
    if not password or len(password) < 1:
        print("\n[%s] No data was altered in your keyring.\n" % (
            colors.rwrap("Canceled")))
        sys.exit()

    # Try to store the password
    username = '%s:%s' % (args.env, args.parameter)
    try:
        store_ok = password_set(username, password)
    except:
        store_ok = False

    if store_ok:
        msg = ("[%s] Successfully stored credentials for %s under the "
               "supernova service.\n")
        print(msg % (colors.gwrap("Success"), username))
    else:
        msg = ("[%s] Unable to store credentials for %s under the "
               "supernova service.\n")
        print(msg % (colors.rwrap("Failed"), username))


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
