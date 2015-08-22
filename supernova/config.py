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
Takes care of the basic setup of the config files and does some preliminary
sanity checks
"""
import os


from configobj import ConfigObj


import six


def run_config(config_file_override=False):
    """
    Runs sanity checks and prepares the global nova_creds variable
    """
    try:
        nova_creds = load_config(config_file_override)
    except:
        raise
    return nova_creds


def load_config(config_file_override=False):
    """
    Pulls the supernova configuration file and reads it
    """
    supernova_config = get_config_file(config_file_override)
    supernova_config_dir = get_config_directory(config_file_override)

    if not supernova_config and not supernova_config_dir:
        raise Exception("Couldn't find a valid configuration file to parse")

    # Can we successfully read the configuration file?
    if supernova_config:
        try:
            nova_creds = ConfigObj(supernova_config)
        except:
            raise ("There is an error in your configuration file, it could not be loaded.")
    else:
        nova_creds = ConfigObj()

    if supernova_config_dir:
        for dir_file in os.listdir(supernova_config_dir):
            full_path = ''.join((supernova_config_dir, dir_file))
            try:
                nova_creds.merge(ConfigObj(full_path))
            except:
                print("Could not parse config file '{}', Skipping.".format(full_path))
    return nova_creds


def get_config_file(override_files=False):
    """
    Looks for the most specific configuration file available.  An override
    can be provided as a string if needed.
    """
    if override_files:
        if isinstance(override_files, six.string_types):
            possible_configs = [override_files]
        else:
            raise Exception("Config file override must be a string")
    else:
        xdg_config_home = os.environ.get('XDG_CONFIG_HOME') or \
            os.path.expanduser('~/.config')
        possible_configs = [os.path.join(xdg_config_home, "supernova"),
                            os.path.expanduser("~/.supernova"),
                            ".supernova"]

    for config_file in reversed(possible_configs):
        if os.path.isfile(config_file):
            return config_file

    return False

def get_config_directory(override_files=False):
    """
    Looks for the most specific configuration directory possible, in order to
    load individual configuration files.
    """
    if override_files:
        if isinstance(override_files, six.string_types):
            possible_configs = [override_files]
        else:
            raise Exception("Config file override must be a string")

    else:       
        xdg_config_home = os.environ.get('XDG_CONFIG_HOME') or \
            os.path.expanduser('~/.config')
        possible_dirs = [os.path.join(xdg_config_home, "supernova.d/"),
                            os.path.expanduser("~/.supernova.d/"),
                            ".supernova.d/"]

    for config_dir in reversed(possible_dirs):
        if os.path.isdir(config_dir):
            return config_dir
    return False

