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


def run_novaclient(nova_creds, nova_args, supernova_args):
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
        nova_args.insert(0, '--debug')

    # Check for OS_EXECUTABLE
    try:
        if env_vars['OS_EXECUTABLE']:
            supernova_args['executable'] = env_vars['OS_EXECUTABLE']
    except KeyError:
        pass

    # Print a small message for the user (very helpful for groups)
    msg = "Running %s against %s..." % (supernova_args.get('executable'),
                                        nova_env)
    print("[%s] %s " % (colors.gwrap('SUPERNOVA'), msg))

    # BYPASS_URL is a weird one, so we need to send it as an argument,
    # not an environment variable.
    bypass_url_args = credentials.add_bypass_url(nova_creds[nova_env])
    if bypass_url_args:
        nova_args = "{0} {1}".format(bypass_url_args, nova_args)

    # Call novaclient and connect stdout/stderr to the current terminal
    # so that any unicode characters from novaclient's list will be
    # displayed appropriately.
    #
    # In other news, I hate how python 2.6 does unicode.
    commandline = "{0} {1}".format(supernova_args['executable'],
                                   nova_args)
    process = subprocess.Popen(shlex.split(commandline),
                               stdout=sys.stdout,
                               stderr=subprocess.PIPE,
                               env=env_vars)

    # Don't exit until we're sure the subprocess has exited
    process.wait()

    stderr_output = process.stderr.read()
    if len(stderr_output) > 0:
        click.secho("\n__ Error Output {0}".format('_'*62), fg='white',
                    bold=True)
        click.echo(stderr_output)

    return process.returncode
