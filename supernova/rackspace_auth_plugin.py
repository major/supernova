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

For use with https://github.com/openstack/python-novaclient

This allows authenication to Rackspace using username and
API key rather than using username and password.

This is for the v2 of Rackspace found at: https://mycloud.rackspace.com/

Example usage:

>>> import rackspace_auth_plugin
>>> cs = client.Client(
    '2', # api version
    'rackspace_username',
    'rackspace_api_key',
    'rackspace_customer_id', # 6 digit number found on the console
    'https://identity.api.rackspacecloud.com/v2.0',
    #region_name='DFW', # Datacentre in Dallas
    region_name='ORD', # Datacentre in Chicago
    auth_system='rackspace',
    auth_plugin=rackspace_auth_plugin,
    )

"""


def authenticate(nova, auth_url):
    """Authenticate to Rackspace using apiKey"""
    payload = {"auth": {
        "RAX-KSKEY:apiKeyCredentials": {
            "username": nova.user,
            "apiKey": nova.password,
            "tenantName": nova.projectid}}}
    return nova._authenticate(auth_url, payload)
