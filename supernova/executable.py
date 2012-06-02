#!/usr/bin/env python
#
# Copyright 2012 Major Hayden
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
import optparse
import supernova
import sys


def gwrap(some_string):
    """
    Returns green text
    """
    return "\033[92m%s\033[0m" % some_string


def rwrap(some_string):
    """
    Returns red text
    """
    return "\033[91m%s\033[0m" % some_string


def print_valid_envs(valid_envs):
    """
    Prints the available environments.
    """
    print "[%s] Your valid environments are:" % (gwrap('Found environments'))
    print "%r" % valid_envs


def run_supernova():
    """
    Handles all of the prep work and error checking for the
    supernova executable.
    """
    s = supernova.SuperNova()
    parser = optparse.OptionParser()
    parser.add_option('--debug', action="store_true",
            dest="debug", default=False,
            help='show novaclient debug output (overrides NOVACLIENT_DEBUG)')

    # Allow for passing --options all the way through to novaclient
    parser.disable_interspersed_args()
    (opts, args) = parser.parse_args()

    # Is the config file missing or empty?
    if s.get_nova_creds() == None:
        print "[%s] Unable to find your supernova configuration file or your " \
              "configuration file is malformed." % (
                    rwrap("Configuration missing"))
        sys.exit()

    # Did we get a valid environment?
    try:
        s.nova_env = args[0]
        if not s.is_valid_environment():
            print "[%s] Unable to find the %r environment in your " \
                  "configuration file.\n" % (
                    rwrap('Invalid environment'), args[0])
            print_valid_envs(sorted(s.get_nova_creds().sections()))
            sys.exit()
    except IndexError:
        print "[%s] A valid nova environment is required as the first " \
              "argument.\n" % (rwrap("Environment missing"))
        print_valid_envs(sorted(s.get_nova_creds().sections()))
        sys.exit()

    # Did we get any arguments to pass on to nova?
    if len(args) <= 1:
        print "[%s] No arguments were provided to pass along to nova." % (
            rwrap('Missing novaclient arguments'))
        sys.exit()

    # All of the remaining arguments should be handed off to nova
    novaclient_args = args[1:]
    s.run_novaclient(novaclient_args, opts.debug)
