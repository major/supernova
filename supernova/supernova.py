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
import os
import subprocess
import sys


import click


from . import credentials


def execute_executable(nova_args, env_vars):
    """
    Executes the executable given by the user.

    Hey, I know this method has a silly name, but I write the code here and
    I'm silly.
    """
    process = subprocess.Popen(nova_args,
                               stdout=sys.stdout,
                               stderr=subprocess.PIPE,
                               env=env_vars)
    process.wait()
    return process


def check_for_executable(supernova_args, env_vars):
    """
    It's possible that a user might set their custom executable via an
    environment variable.  If we detect one, we should add it to supernova's
    arguments ONLY IF an executable wasn't set on the command line.  The
    command line executable must take priority.
    """
    exe = supernova_args.get('executable', 'default')
    if exe != 'default':
        return supernova_args
    if 'OS_EXECUTABLE' in env_vars.keys():
        supernova_args['executable'] = env_vars['OS_EXECUTABLE']
        return supernova_args
    supernova_args['executable'] = 'nova'
    return supernova_args


def check_for_bypass_url(raw_creds, nova_args):
    """
    Return a list of extra args that need to be passed on cmdline to nova.
    """
    if 'BYPASS_URL' in raw_creds.keys():
        bypass_args = ['--bypass-url', raw_creds['BYPASS_URL']]
        nova_args = bypass_args + nova_args

    return nova_args


def handle_stderr(stderr_pipe):
    """
    Takes stderr from the command's output and displays it AFTER the stdout
    is printed by run_command().
    """
    stderr_output = stderr_pipe.read()

    if len(stderr_output) > 0:
        click.secho("\n__ Error Output {0}".format('_'*62), fg='white',
                    bold=True)
        click.echo(stderr_output)

    return True


def run_command(nova_creds, nova_args, supernova_args):
    """
    Sets the environment variables for the executable, runs the executable,
    and handles the output.
    """
    nova_env = supernova_args['nova_env']

    # Get the environment variables ready
    env_vars = os.environ.copy()
    env_vars.update(credentials.prep_shell_environment(nova_env,
                                                       nova_creds))
    # Check for a debug override
    if supernova_args['debug']:
        nova_args.insert(0, '--debug ')

    # BYPASS_URL is a weird one, so we need to send it as an argument,
    # not an environment variable.
    nova_args = check_for_bypass_url(nova_creds[nova_env], nova_args)

    # Check for OS_EXECUTABLE
    supernova_args = check_for_executable(supernova_args, env_vars)

    # Print a small message for the user (very helpful for groups)
    msg = "Running %s against %s..." % (supernova_args.get('executable'),
                                        nova_env)
    if not supernova_args.get('quiet'):
        click.echo("[%s] %s " % (click.style('SUPERNOVA', fg='green'), msg))

    # Call executable and connect stdout to the current terminal
    # so that any unicode characters from the executable's list will be
    # displayed appropriately.
    #
    # In other news, I hate how python 2.6 does unicode.
    nova_args.insert(0, supernova_args['executable'])
    process = execute_executable(nova_args, env_vars)

    # If the user asked us to be quiet, then let's not print stderr
    if not supernova_args.get('quiet'):
        handle_stderr(process.stderr)

    return process.returncode
