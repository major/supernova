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
Contains the actual class that runs novaclient (or the executable chosen by
the user)
"""
from __future__ import print_function


import os
import shlex
import subprocess
import sys


import click


from . import colors
from . import credentials


def execute_executable(commandline, env_vars):
    """
    Executes the executable given by the user.

    Hey, I know this method has a silly name, but I write the code here and
    I'm silly.
    """
    process = subprocess.Popen(shlex.split(commandline),
                               stdout=sys.stdout,
                               stderr=subprocess.PIPE,
                               env=env_vars)
    process.wait()
    return process


def check_for_executable(supernova_args, env_vars):
    if 'OS_EXECUTABLE' in env_vars.keys():
        supernova_args['executable'] = env_vars['OS_EXECUTABLE']

    return supernova_args


def check_for_bypass_url(raw_creds):
    """
    Return a list of extra args that need to be passed on cmdline to nova.
    """
    if 'BYPASS_URL' in raw_creds.keys():
        args = '--bypass-url {0}'.format(raw_creds['BYPASS_URL'])
    else:
        args = ''

    return args


def handle_stderr(stderr_pipe):
    stderr_output = stderr_pipe.read()

    if len(stderr_output) > 0:
        click.secho("\n__ Error Output {0}".format('_'*62), fg='white',
                    bold=True)
        click.echo(stderr_output)

    return True


def run_command(nova_creds, nova_args, supernova_args):
    """
    Sets the environment variables for novaclient, runs novaclient, and
    prints the output.

    NOTE(major): The name of this method is a bit misleading.  By using the
    OS_EXECUTABLE environment variable or the -x argument, a user can
    specify a different executable to be used other than the default, which
    is 'nova'.
    """
    nova_env = supernova_args['nova_env']

    # Get the environment variables ready
    env_vars = os.environ.copy()
    env_vars.update(credentials.prep_shell_environment(nova_env,
                                                       nova_creds))

    # Check for a debug override
    if supernova_args['debug']:
        nova_args = '--debug ' + nova_args

    # Check for OS_EXECUTABLE
    supernova_args = check_for_executable(supernova_args, env_vars)

    # Print a small message for the user (very helpful for groups)
    msg = "Running %s against %s..." % (supernova_args.get('executable'),
                                        nova_env)
    print("[%s] %s " % (colors.gwrap('SUPERNOVA'), msg))

    # BYPASS_URL is a weird one, so we need to send it as an argument,
    # not an environment variable.
    bypass_url_args = check_for_bypass_url(nova_creds[nova_env])
    nova_args = "{0} {1}".format(bypass_url_args, nova_args)

    # Call executable and connect stdout to the current terminal
    # so that any unicode characters from the executable's list will be
    # displayed appropriately.
    #
    # In other news, I hate how python 2.6 does unicode.
    commandline = "{0} {1}".format(supernova_args['executable'],
                                   nova_args)
    process = execute_executable(commandline, env_vars)
    handle_stderr(process.stderr)

    return process.returncode
