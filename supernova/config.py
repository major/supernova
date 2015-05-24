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
try:
    import ConfigParser
except:
    import configparser as ConfigParser

import os
import sys


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
    create_dynamic_configs(supernova_config)

    # Can we successfully read the configuration file?
    try:
        nova_creds = ConfigObj(supernova_config)
    except:
        raise

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

    raise Exception("Couldn't find a valid configuration file to parse")

    return nova_creds


def create_dynamic_configs(config, key='OS_REGION_NAME', delimiter=';'):
    sections = config.sections()
    for section in sections:

        # Check to see if we should generate new sections.
        if config.has_option(section, key) and delimiter in \
                config.get(section, key):

            for new_section_arg in config.get(section, key).split(
                    delimiter):
                try:
                    new_section = section + '-' + new_section_arg
                    config.add_section(new_section)

                    # We are eventually going to delete the old section.
                    # Lets use it as a supernova group
                    config.set(new_section, 'SUPERNOVA_GROUP', section)

                    for orig_section_key, orig_section_value in \
                            config.items(section):
                        if orig_section_key.lower() == key.lower():
                            config.set(new_section, orig_section_key,
                                       new_section_arg)
                        else:
                            config.set(new_section, orig_section_key,
                                       orig_section_value)
                except ConfigParser.DuplicateSectionError:
                    # Skip, in case it already exists or the user has defined
                    # it
                    pass
            # We are done, lets remove the original section
            config.remove_section(section)
