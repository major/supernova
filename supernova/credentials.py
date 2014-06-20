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
import keyring
import re
import sys

from . import colors


def get_user_password(args):
    """
    Allows the user to print the credential for a particular keyring entry
    to the screen
    """
    username = '%s:%s' % (args.env, args.parameter)

    warnstring = colors.rwrap("__ WARNING ".ljust(80, '_'))
    print("""
%s

If this operation is successful, the credential stored for this username will
be displayed in your terminal as PLAIN TEXT:

  %s

Seriously.  It will just be hanging out there for anyone to see.  If you have
any concerns about having this credential displayed on your screen, press
CTRL-C right now.

%s
""" % (warnstring, username, warnstring))
    print("If you are completely sure you want to display it, type 'yes' and ",
          "press enter:")
    try:
        if sys.version_info.major >= 3:
            confirm = input('')
        else:
            confirm = raw_input('')
    except KeyboardInterrupt:
        print('')
        confirm = ''
    if confirm != 'yes':
        print("\n[%s] Your keyring was not read or altered.\n" % (
            colors.rwrap("Canceled")))
        return False

    try:
        password = password_get(username)
    except:
        password = None

    if password:
        print("""
[%s] Found credentials for %s: %s
""" % (
            colors.gwrap("Success"), username, password))
        return True
    else:
        print("""
[%s] Unable to retrieve credentials for %s.

It's likely that there aren't any credentials stored for this environment and
parameter combination.  If you want to set a credential, just run this command:

  supernova-keyring -s %s %s
""" % (colors.rwrap("Failed"), username, args.env, args.parameter))
        return False


def pull_env_credential(env, param, value):
    """
    Dissects a keyring credential lookup string from the supernova config file
    and returns the username/password combo
    """
    rex = "USE_KEYRING\[([\x27\x22])(.*)\\1\]"
    if value == "USE_KEYRING":
        username = "%s:%s" % (env, param)
    else:
        global_identifier = re.match(rex, value).group(2)
        username = "%s:%s" % ('global', global_identifier)
    return (username, password_get(username))


def password_get(username=None):
    """
    Retrieves a password from the keychain based on the environment and
    configuration parameter pair.
    """
    try:
        return keyring.get_password('supernova', username).encode('ascii')
    except:
        return False


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
