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
Contains the functions needed for supernova and supernova-keyring commands
to run
"""
from __future__ import print_function

import argparse
import sys


import click


import pkg_resources


from . import colors
from . import config
from . import credentials
from . import supernova
from . import utils


def print_version(ctx, param, value):
    version = pkg_resources.require("supernova")[0].version
    click.echo("supernova %s" % version)
    ctx.exit()


def print_env_list(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    config.run_config()
    for nova_env in config.nova_creds.sections():
        envheader = '-- %s ' % colors.gwrap(nova_env)
        print(envheader.ljust(86, '-'))
        for param, value in sorted(config.nova_creds.items(nova_env)):
            print('  %s: %s' % (param.upper().ljust(21), value))
    ctx.exit()


@click.command()
@click.option('--executable', '-x', default='nova',
              help='command to run', show_default=True)
@click.option('--debug', '-d', default='False', is_flag=True,
              help="Enable debugging", show_default=True)
@click.argument('environment', nargs=1)
@click.argument('command')
@click.version_option(prog_name='supernova')
@click.option('--list', is_flag=True, callback=print_env_list,
              expose_value=False, is_eager=False, default=False,
              help="List all configured environments")
@click.pass_context
def run_supernova(ctx, executable, debug, environment, command):
    """
    Handles all of the prep work and error checking for the
    supernova executable.
    """
    config.run_config()

    # Did we get any arguments to pass on to nova?
    if not command:
        utils.warn_missing_nova_args()
        sys.exit(1)

    # Is our environment argument a single environment or a supernova group?
    if utils.is_valid_group(environment):
        envs = utils.get_envs_in_group(environment)
    else:
        envs = [environment]

    supernova_args = {
        'debug': debug,
        'executable': executable
    }

    for env in envs:
        snobj = supernova.SuperNova()
        snobj.nova_env = env
        returncode = snobj.run_novaclient(command, supernova_args)

    # NOTE(major): The return code here is the one that comes back from the
    # OS_EXECUTABLE that supernova runs (by default, 'nova').  When using
    # supernova groups, the return code is the one returned by the executable
    # for the last environment in the group.
    #
    # It's not ideal, but it's all I can think of for now. ;)
    sys.exit(returncode)


def run_supernova_keyring():
    """
    Handles all of the prep work and error checking for the
    supernova-keyring executable.
    """
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-g', '--get', action='store_true',
                       dest='get_password',
                       help='retrieves credentials from keychain storage')
    group.add_argument('-s', '--set', action='store_true',
                       dest='set_password',
                       help='stores credentials in keychain storage')
    parser.add_argument('env',
                        help='environment to set parameter in')
    parser.add_argument('parameter',
                        help='parameter to set')
    args = parser.parse_args()

    if args.set_password:
        credentials.set_user_password(args)

    if args.get_password:
        credentials.get_user_password(args)
