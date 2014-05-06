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
import sys


from colors import gwrap, rwrap
import config


def check_deprecated_options(self):
    """
    Hunts for deprecated configuration options from previous SuperNova
    versions.
    """
    creds = config.nova_creds
    if creds.has_option(self.nova_env, 'insecure'):
        print "WARNING: the 'insecure' option is deprecated. " \
              "Consider using NOVACLIENT_INSECURE=1 instead."


def get_envs_in_group(group_name):
    envs = []
    for section in config.nova_creds.sections():
        if (config.nova_creds.has_option(section, 'SUPERNOVA_GROUP') and
                config.nova_creds.get(section,
                                    'SUPERNOVA_GROUP') == group_name):
            envs.append(section)
    return envs

def is_valid_environment(self):
    """
    Checks to see if the configuration file contains a section for our
    requested environment.
    """
    valid_envs = config.nova_creds.sections()
    return self.nova_env in valid_envs

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
    print "[%s] Your valid environments are:" % (gwrap('Found environments'))
    print "%r" % valid_envs

def warn_missing_nova_args():
    msg = """
[%s] No arguments were provided to pass along to nova.
The supernova script expects to get commands structured like this:

  supernova [environment] [command]

Here are some example commands that may help you get started:

  supernova prod list
  supernova prod image-list
  supernova prod keypair-list
"""
    print msg % rwrap('Missing arguments')

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
