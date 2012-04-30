#!/usr/bin/python
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
import ConfigParser
import os
import subprocess
import sys


# Helps us find non-python files installed by setuptools
def data_file(fname):
    """Return the path to a data file of ours."""
    return os.path.join(os.path.split(__file__)[0], fname)

# Pick up the user's credentials and environments
user_creds = ConfigParser.RawConfigParser()
user_creds.read([os.path.expanduser("~/.supernova"), '.supernova'])


def bin_helper():
    # Parse any options the user might have passed
    args = sys.argv
    args.pop(0)  # get rid of the PROG arg
    while True:
        try:
            nova_env = args.pop(0)  # environment argument for supernova
        except IndexError:
            print "You must specify a valid nova environment as " \
                "the first argument."
            print "Available environments: %r" % nova_envs.sections()
            sys.exit()
        # make the sneakies on "supernova debug nova_env list"
        if nova_env == 'debug':
            # note this doesn't "export" the var, it only effects this process
            os.environ['NOVACLIENT_DEBUG'] = '1'
        else:
            break

    # Does the user have a configuration block for this environment?
    if nova_env not in user_creds.sections():
        print "You asked for the %r environment but it doesn't " \
            "have a configuration section starting with [%s] in %s." % (
            nova_env, nova_env, os.path.expanduser("~/.supernova"))
        sys.exit()

    # Our remaining arguments should be the stuff we pass through to
    # novaclient
    if len(args) < 1:
        print "You didn't provide any arguments to pass through " \
            "to novaclient."
        sys.exit()
    else:
        nova_args = args

    # Do we have any login credentials for the environment specified?
    if not any(k for (k, v) in user_creds.items(nova_env) if k.endswith('_url')):
        print """
You may be missing authentication credentials for the %r environment in your
%s file.  Newer versions of supernova require all of your novaclient
environment variables to be present in %s.
""" % (nova_env, os.path.expanduser("~/.supernova"),
            os.path.expanduser("~/.supernova"))

    # Get our environment variables ready
    # novaclient compatibility note - if your values are surrounded by ""
    # or '', those characters will be stripped automatically below
    env = os.environ
    for key, value in user_creds.items(nova_env):
        if key == "insecure":
            continue
        env[key.upper()] = value.strip("\"'")

    # Do we need to call nova with --insecure for this environment?
    if user_creds.has_option(nova_env, 'insecure'):
        nova_args = ['--insecure'] + nova_args

    # Call novaclient
    p = subprocess.Popen(['nova'] + nova_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env
    )

    # Print novaclient's output
    for line in p.stdout:
        print line.rstrip("\n")
