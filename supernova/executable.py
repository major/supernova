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
    for nova_env in config.nova_creds.keys():
        envheader = '-- %s ' % colors.gwrap(nova_env)
        print(envheader.ljust(86, '-'))
        for param, value in sorted(config.nova_creds[nova_env].items()):
            print('  %s: %s' % (param.upper().ljust(25), value))
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

    utils.check_environment_presets()

    # Did we get any arguments to pass on to nova?
    if not command:
        msg = """
[%s] No arguments were provided to pass along to nova.
The supernova script expects to get commands structured like this:

  supernova [environment] [command]

Here are some example commands that may help you get started:

  supernova prod list
  supernova prod image-list
  supernova prod keypair-list"""
        click.echo(msg)
        ctx.exit()

    # Is our environment argument a single environment or a supernova group?
    if utils.is_valid_group(environment, config.nova_creds):
        envs = utils.get_envs_in_group(environment, config.nova_creds)
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


@click.command()
@click.option('--get', '-g', 'action', flag_value='get_credential',
              help='retrieve a credential from keyring storage')
@click.option('--set', '-s', 'action', flag_value='set_credential',
              help='store a credential in keyring storage',)
@click.argument('environment', nargs=1)
@click.argument('parameter', nargs=1)
@click.pass_context
def run_supernova_keyring(ctx, action, environment, parameter):
    """
    Sets or retrieves credentials stored in your system's keyring using the
    python-keyring module.

    Consider a supernova configuration file with these items:

    \b
        [prod]
        OS_PASSWORD=USE_KEYRING['production_sso']
        ...

    You could retrieve or set the credential using these commands:

    \b
        supernova -g prod production_sso     <= get the credential
        supernova -s prod production_sso     <= set the credential
    """
    if action is None:
        click.secho("ERROR: must specify --get or --set", bold=True)
        click.echo(ctx.get_help())
        ctx.exit()

    if action == 'get_credential':
        result = credentials.get_user_password(env=environment,
                                               param=parameter)
        if not result:
            click.echo("\nUnable to find a credential matching the data "
                       "provided.")
        else:
            click.echo("\nFound credential for {0}: {1}".format(*result))
        ctx.exit()

    if action == 'set_credential':
        msg = """
Preparing to set a credential in the keyring for:

  - Environment  : {0}
  - Parameter    : {1}

If this is correct, enter the corresponding credential to store in your keyring
or press CTRL-C to abort""".format(environment, parameter)
        credential = click.prompt(text=msg, hide_input=True)

        result = credentials.set_user_password(environment=environment,
                                               parameter=parameter,
                                               password=credential)

        if result:
            click.echo("\nSuccessfully stored.")
        else:
            click.echo("\nUnable to store your credential.")
        ctx.exit()
