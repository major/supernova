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
import argparse
import ConfigParser
import os
import sys

from colors import gwrap, rwrap

nova_creds = None

def run_config():
    global nova_creds
    check_environment_presets()
    nova_creds = load_supernova_config()

def check_environment_presets():
    presets = [x for x in os.environ.copy().keys() if x.startswith('NOVA_') or
               x.startswith('OS_')]
    if len(presets) < 1:
        pass
    else:
        print "_" * 80
        print "*WARNING* Found existing environment variables that may "\
              "cause conflicts:"
        for preset in presets:
            print "  - %s" % preset
        print "_" * 80

def load_supernova_config():
    possible_configs = [os.path.expanduser('~/.supernova'), '.supernova']
    nova_creds = ConfigParser.RawConfigParser()

    # Can we successfully read the configuration file?
    try:
        nova_creds.read(possible_configs)
    except:
        msg = """
[%s] A valid supernova configuration file is required.
Ensure that you have a properly configured supernova configuration file called
'.supernova' in your home directory or in your current working directory.
""" % rwrap('Invalid configuration file')
        print msg
        sys.exit(1)

    return nova_creds
