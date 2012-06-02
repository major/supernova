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
import ConfigParser
import keyring
import os
import re
import subprocess


__version__ = '0.6.1'


class SuperNova:

    def __init__(self):
        self.nova_creds = None
        self.nova_env = None
        self.env = os.environ

    def check_deprecated_options(self):
        """
        Hunts for deprecated configuration options from previous SuperNova
        versions.
        """
        creds = self.get_nova_creds()
        if creds.has_option(self.nova_env, 'insecure'):
            print "WARNING: the 'insecure' option is deprecated. " \
                  "Consider using NOVACLIENT_INSECURE=1 instead."

    def get_nova_creds(self):
        """
        Reads the supernova config file from the current directory or the
        user's home directory.  If the config file has already been read, the
        cached copy is immediately returned.
        """
        if self.nova_creds:
            return self.nova_creds

        possible_configs = [os.path.expanduser("~/.supernova"), '.supernova']
        self.nova_creds = ConfigParser.RawConfigParser()
        self.nova_creds.read(possible_configs)
        if len(self.nova_creds.sections()) < 1:
            return None
        return self.nova_creds

    def is_valid_environment(self):
        """
        Checks to see if the configuration file contains a section for our
        requested environment.
        """
        valid_envs = self.get_nova_creds().sections()
        return self.nova_env in valid_envs

    def password_get(self, username=None):
        """
        Retrieves a password from the keychain based on the environment and
        configuration parameter pair.
        """
        try:
            return keyring.get_password('supernova', username)
        except:
            return False

    def password_set(self, username=None, password=None):
        """
        Stores a password in a keychain for a particular environment and
        configuration parameter pair.
        """
        try:
            keyring.set_password('supernova', username, password)
            return True
        except:
            return False

    def prep_nova_creds(self):
        """
        Finds relevant config options in the supernova config and cleans them
        up for novaclient.
        """
        self.check_deprecated_options()
        raw_creds = self.get_nova_creds().items(self.nova_env)
        nova_re = re.compile(r"(^nova_|^os_|^novaclient)")

        creds = []
        for param, value in raw_creds:

            # Skip parameters we're unfamiliar with
            if not nova_re.match(param):
                continue

            param = param.upper()

            # Get values from the keyring if we find a USE_KEYRING constant
            if value == "USE_KEYRING":
                username = "%s:%s" % (self.nova_env, param)
                value = self.password_get(username)
            else:
                value = value.strip("\"'")

            # Make sure we got something valid from the configuration file or
            # the keyring
            if not value:
                msg = "Attempted to retrieve a credential for %s but " \
                      "couldn't find it within the keyring." % username
                raise Exception(msg)

            creds.append((param, value))

        return creds

    def prep_shell_environment(self):
        """
        Appends new variables to the current shell environment temporarily.
        """
        for k, v in self.prep_nova_creds():
            self.env[k] = v

    def run_novaclient(self, nova_args, force_debug=False):
        """
        Sets the environment variables for novaclient, runs novaclient, and
        prints the output.
        """
        self.prep_shell_environment()
        if force_debug:
            self.env['NOVACLIENT_DEBUG'] = '1'
        p = subprocess.Popen(['nova'] + nova_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=self.env
        )
        for line in p.stdout:
            print line.rstrip("\n")
