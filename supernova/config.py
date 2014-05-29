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

from . import colors

nova_creds = None


def run_config():
    """
    Runs sanity checks and prepares the global nova_creds variable
    """
    global nova_creds
    check_environment_presets()
    nova_creds = load_supernova_config()


def check_environment_presets():
    """
    Checks for environment variables that can cause problems with supernova
    """
    presets = [x for x in os.environ.copy().keys() if x.startswith('NOVA_') or
               x.startswith('OS_')]
    if len(presets) < 1:
        return True
    else:
        print("_" * 80)
        print("*WARNING* Found existing environment variables that may ",
              "cause conflicts:")
        for preset in presets:
            print("  - %s" % preset)
        print("_" * 80)
        return False


def load_supernova_config():
    """
    Pulls the supernova configuration file and reads it
    """
    xdg_config_home = os.environ.get('XDG_CONFIG_HOME') or \
        os.path.expanduser('~/.config')
    possible_configs = [os.path.join(xdg_config_home, "supernova"),
                        os.path.expanduser("~/.supernova"),
                        ".supernova"]
    supernova_config = ConfigParser.RawConfigParser()

    # Can we successfully read the configuration file?
    try:
        supernova_config.read(possible_configs)
    except:
        msg = """
[%s] A valid supernova configuration file is required.
Ensure that you have a properly configured supernova configuration file called
'.supernova' in your home directory or in your current working directory.
""" % colors.rwrap('Invalid configuration file')
        print(msg)
        sys.exit(1)

    return supernova_config
