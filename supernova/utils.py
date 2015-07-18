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
import os


import click


def assemble_username(env, param):
    return "{0}:{1}".format(env, param)


def check_environment_presets():
    """
    Checks for environment variables that can cause problems with supernova
    """
    presets = [x for x in os.environ.copy().keys() if x.startswith('NOVA_') or
               x.startswith('OS_')]
    if len(presets) < 1:
        return True
    else:
        click.echo("_" * 80)
        click.echo("*WARNING* Found existing environment variables that may "
                   "cause conflicts:")
        for preset in presets:
            click.echo("  - %s" % preset)
        click.echo("_" * 80)
        return False


def confirm_credential_display(force=False):
    if force:
        return True

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


def is_valid_environment(env, nova_creds):
    """
    Checks to see if the configuration file contains a section for our
    requested environment.
    """
    if env in nova_creds.keys():
        return env
    else:
        return False


def is_valid_group(group_name, nova_creds):
    """
    Checks to see if the configuration file contains a SUPERNOVA_GROUP
    configuration option.
    """
    valid_groups = [value['SUPERNOVA_GROUP'] for key, value in
                    nova_creds.items() if 'SUPERNOVA_GROUP'
                    in nova_creds[key].keys()]
    if group_name in valid_groups:
        return True
    else:
        return False


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
