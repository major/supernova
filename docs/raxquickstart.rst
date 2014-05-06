Rackspace Quick Start
=====================================

If you're already a Rackspace customer, you can get started quickly with supernova by following these steps::

    pip install supernova rackspace-novaclient
    wget -O ~/.supernova http://bit.ly/raxsupernova
    supernova-keyring -s global RackspaceAccountUser
    supernova-keyring -s global RackspaceAccountAPIKey
    supernova-keyring -s global RackspaceAccountDDI
    supernova dfw list

Let's break down these steps one by one.

We start by installing supernova as well as rackspace-novaclient (which is required for novaclient to talk to Rackspace's identity API)::

    pip install supernova rackspace-novaclient

There's a `Rackspace example configuration <http://bit.ly/raxsupernova>`_ file in the main repository and we can store that in our home directory as `.supernova`::

    wget -O ~/.supernova http://bit.ly/raxsupernova

One of supernova's features is the ability to store sensitive data in your operating system's keyring.  This also makes it handy when you want to re-use usernames, account numbers and passwords across multiple environments.  We add that data to the keyring with these commands::

    supernova-keyring -s global RackspaceAccountUser
    supernova-keyring -s global RackspaceAccountAPIKey
    supernova-keyring -s global RackspaceAccountDDI

Finally, we can test our configuration by listing our current instances in the DFW region::

    supernova dfw list