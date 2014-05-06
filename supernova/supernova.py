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
import ConfigParser
import keyring
from novaclient import client as novaclient
import os
import re
import subprocess
import sys


import config
import credentials


class SuperNova:

    def __init__(self):
        config.run_config()
        self.nova_env = None
        self.env = os.environ.copy()

    def prep_nova_creds(self):
        """
        Finds relevant config options in the supernova config and cleans them
        up for novaclient.
        """
        raw_creds = config.nova_creds.items(self.nova_env)
        nova_re = re.compile(r"(^nova_|^os_|^novaclient|^trove_)")

        creds = []
        for param, value in raw_creds:

            # Skip parameters we're unfamiliar with
            if not nova_re.match(param):
                continue

            param = param.upper()

            # Get values from the keyring if we find a USE_KEYRING constant
            if value.startswith("USE_KEYRING"):
                credential = credentials.pull_env_credential(value)
            else:
                credential = value.strip("\"'")

            # Make sure we got something valid from the configuration file or
            # the keyring
            if not credential:
                msg = """
While connecting to %s, supernova attempted to retrieve a credential
for %s but couldn't find it within the keyring.  If you haven't stored
credentials for %s yet, try running:

    supernova-keyring -s %s
""" % (self.nova_env, username, username, ' '.join(username.split(':')))
                print msg
                sys.exit(1)

            creds.append((param, credential))

        return creds

    def prep_shell_environment(self):
        """
        Appends new variables to the current shell environment temporarily.
        """
        # self.env = os.environ.copy()
        for k, v in self.prep_nova_creds():
            self.env[k] = v

    def run_novaclient(self, nova_args, supernova_args):
        """
        Sets the environment variables for novaclient, runs novaclient, and
        prints the output.
        """
        # Get the environment variables ready
        self.prep_shell_environment()

        # Check for a debug override
        if supernova_args.debug:
            nova_args.insert(0, '--debug')

        # Check for OS_EXECUTABLE
        try:
            if self.env['OS_EXECUTABLE']:
                supernova_args.executable = self.env['OS_EXECUTABLE']
        except KeyError:
            pass

        # Print a small message for the user (very helpful for groups)
        msg = "Running %s against %s..." % (supernova_args.executable,
                                            self.nova_env)
        print "[SUPERNOVA] %s " % msg

        # Call novaclient and connect stdout/stderr to the current terminal
        # so that any unicode characters from novaclient's list will be
        # displayed appropriately.
        #
        # In other news, I hate how python 2.6 does unicode.
        p = subprocess.Popen([supernova_args.executable] + nova_args,
                             stdout=sys.stdout,
                             stderr=sys.stderr,
                             env=self.env)

        # Don't exit until we're sure the subprocess has exited
        return p.wait()

    def get_novaclient(self, env, client_version=3):
        """
        Returns python novaclient object authenticated with supernova config.
        """
        self.nova_env = env
        assert self.is_valid_environment(), "Env %s not found in config." % env
        print "Getting novaclient!"
        return novaclient.Client(client_version, **self.prep_python_creds())

    def prep_python_creds(self):
        """
        Prepare credentials for python Client instantiation.
        """
        creds = dict((utils.rm_prefix(k[0].lower()), k[1])
                     for k in self.prep_nova_creds())
        if creds.get('url'):
            creds['auth_url'] = creds.pop('url')
        if creds.get('tenant_name'):
            creds['project_id'] = creds.pop('tenant_name')
        return creds
