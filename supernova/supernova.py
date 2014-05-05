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
import rackspace_auth_plugin
import re
import subprocess
import sys


import credentials


class SuperNova:

    def __init__(self):
        self.nova_creds = None
        self.nova_env = None
        self.env = os.environ.copy()

        # Check for preset environment variables that could cause problems
        self.check_environment_presets()

    def check_deprecated_options(self):
        """
        Hunts for deprecated configuration options from previous SuperNova
        versions.
        """
        creds = self.get_nova_creds()
        if creds.has_option(self.nova_env, 'insecure'):
            print "WARNING: the 'insecure' option is deprecated. " \
                  "Consider using NOVACLIENT_INSECURE=1 instead."

    def check_environment_presets(self):
        presets = [x for x in self.env.keys() if x.startswith('NOVA_') or
                   x.startswith('OS_')]
        if len(presets) < 1:
            pass
        else:
            print "_" * 80
            print "*WARNING* Found existing environment variables that may "\
                  "cause conflicts:"
            for preset in presets:
                print "  - %s" % preset
            print "_" * 80

    def get_envs_in_group(self, group_name):
        envs = []
        for section in self.nova_creds.sections():
            if (self.nova_creds.has_option(section, 'SUPERNOVA_GROUP') and
                    self.nova_creds.get(section,
                                        'SUPERNOVA_GROUP') == group_name):
                envs.append(section)
        return envs

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

    def is_valid_group(self, group_name):
        """
        Checks to see if the configuration file contains a SUPERNOVA_GROUP
        configuration option.
        """
        valid_groups = []
        for section in self.nova_creds.sections():
            if self.nova_creds.has_option(section, 'SUPERNOVA_GROUP'):
                valid_groups.append(self.nova_creds.get(section,
                                                        'SUPERNOVA_GROUP'))
        valid_groups = list(set(valid_groups))
        if group_name in valid_groups:
            return True
        else:
            return False

    def prep_nova_creds(self):
        """
        Finds relevant config options in the supernova config and cleans them
        up for novaclient.
        """
        self.check_deprecated_options()
        raw_creds = self.get_nova_creds().items(self.nova_env)
        nova_re = re.compile(r"(^nova_|^os_|^novaclient|^trove_)")

        creds = []
        for param, value in raw_creds:

            # Skip parameters we're unfamiliar with
            if not nova_re.match(param):
                continue

            param = param.upper()

            # Get values from the keyring if we find a USE_KEYRING constant
            if value.startswith("USE_KEYRING"):
                rex = "USE_KEYRING\[([\x27\x22])(.*)\\1\]"
                if value == "USE_KEYRING":
                    username = "%s:%s" % (self.nova_env, param)
                else:
                    global_identifier = re.match(rex, value).group(2)
                    username = "%s:%s" % ('global', global_identifier)
                credential = credentials.password_get(username)
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
        self.env = os.environ.copy()
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

        # Print a small message for the user
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

    def get_novaclient(self, env):
        """
        Returns python novaclient object authenticated with supernova config.
        """
        self.nova_env = env
        assert self.is_valid_environment(), "Env %s not found in config." % env
        return novaclient.Client(**self.prep_python_creds())

    def prep_python_creds(self):
        """
        Prepare credentials for python Client instantiation.
        """
        creds = dict((rm_prefix(k[0].lower()), k[1])
                     for k in self.prep_nova_creds())
        if creds.get('auth_system') == 'rackspace':
            creds['auth_plugin'] = rackspace_auth_plugin
        if creds.get('url'):
            creds['auth_url'] = creds.pop('url')
        if creds.get('tenant_name'):
            creds['project_id'] = creds.pop('tenant_name')
        return creds


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
