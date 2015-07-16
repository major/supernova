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
Contains many of the shared utility functions
"""
from __future__ import print_function


import click


from . import colors
from . import config


def assemble_username(env, param):
    return "{0}:{1}".format(env, param)


def confirm_credential_display():
    msg = """
    [WARNING] Your credential is about to be displayed on screen.
    If this is really what you want, type 'y' and press enter."""
    result = click.confirm(text=msg)
    return result


def get_envs_in_group(group_name, nova_creds):
    """
    Takes a group_name and finds any environments that have a SUPERNOVA_GROUP
    configuration line that matches the group_name.
    """
    envs = []
    for section in nova_creds.keys():
        if ('SUPERNOVA_GROUP' in nova_creds[section] and
                nova_creds[section]['SUPERNOVA_GROUP'] == group_name):
            envs.append(section)
    return envs


def is_valid_environment(env):
    """
    Checks to see if the configuration file contains a section for our
    requested environment.
    """
    valid_envs = config.nova_creds.sections()
    return env in valid_envs


def is_valid_group(group_name):
    """
    Checks to see if the configuration file contains a SUPERNOVA_GROUP
    configuration option.
    """
    valid_groups = []
    for section in config.nova_creds.sections():
        if config.nova_creds.has_option(section, 'SUPERNOVA_GROUP'):
            valid_groups.append(config.nova_creds.get(section,
                                                      'SUPERNOVA_GROUP'))
    valid_groups = list(set(valid_groups))
    if group_name in valid_groups:
        return True
    else:
        return False


def print_valid_envs(valid_envs):
    """
    Prints the available environments.
    """
    print("[%s] Your valid environments are:" %
          (colors.gwrap('Found environments')))
    print("%r" % valid_envs)


def warn_missing_nova_args():
    """
    Provides a friendly warning for users who forget to provide commands to
    be passed on to nova.
    """
    msg = """
[%s] No arguments were provided to pass along to nova.
The supernova script expects to get commands structured like this:

  supernova [environment] [command]

Here are some example commands that may help you get started:

  supernova prod list
  supernova prod image-list
  supernova prod keypair-list
"""
    print(msg % colors.rwrap('Missing arguments'))


def rm_prefix(name):
    """
    Removes nova_ os_ novaclient_ prefix from string.
    """
    if name.startswith('nova_'):
        return name[5:]
    elif name.startswith('novaclient_'):
        return name[11:]
    elif name.startswith('os_'):
        return name[3:]
    else:
        return name
