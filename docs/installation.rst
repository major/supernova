Installing supernova
=====================================

There are multiple options for installing supernova depending on whether you want to run a stable release or the latest available code.

Getting stable releases from PyPi
---------------------------------

If you're installing for the first time, you can install supernova using pip::

    pip install supernova

Be sure to install rackspace-novaclient if you plan to use supernova with Rackspace's Cloud Servers environments::

    pip install supernova rackspace-novaclient

Upgrading supernova is easy as well::

    pip install -U supernova

Latest available releases from GitHub
-------------------------------------

You can install the latest available version of supernova from GitHub using pip::

    pip install git+git://github.com/major/supernova.git

You can also clone the repository and install supernova::

    git clone https://github.com/major/supernova.git
    cd supernova
    python setup.py install