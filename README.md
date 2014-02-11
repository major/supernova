## supernova - use novaclient with multiple nova environments the easy way

You may like *supernova* if you regularly have the following problems:

* You hate trying to source multiple novarc files when using *nova*
* You get your terminals confused and do the wrong things in the wrong nova environment
* You don't like remembering things
* You want to keep sensitive API keys and passwords out of plain text configuration files (see the "Working with keyrings" section toward the end)
* You need to share common skeleton environment variables for *nova* with your teams

If any of these complaints ring true, *supernova* is for you. *supernova* manages multiple nova environments without sourcing novarc files or mucking with environment variables.

![First world problems - nova style](http://i.imgur.com/CLYY05E.jpg)

### Installation

You will need to have a specific version of the [keyring](https://pypi.python.org/pypi/keyring) python module installed for *supernova* to work but it should be installed automatically when you install *supernova* using the instructions below.

For generic OpenStack environments:

    git clone git://github.com/major/supernova.git
    cd supernova
    python setup.py install

For use with Rackspace Cloud:

    git clone git://github.com/major/supernova.git
    cd supernova
    python setup.py install
    pip install rackspace-novaclient

### Configuration

For *supernova* to work properly, each environment must be defined in `~/.supernova` (a file in your user's home directory).  The data in the file is exactly the same as the environment variables which you would normally use when running *nova*.  You can copy/paste from your `.novarc` files directly into configuration sections within your `~/.supernova` file.

Here's an example of how to use supernova with [Rackspace Cloud Servers](http://www.rackspace.com/cloud/servers/) in different datacenters:

    [iad]
	OS_AUTH_URL=https://identity.api.rackspacecloud.com/v2.0/
	NOVA_RAX_AUTH=1
	OS_AUTH_SYSTEM=rackspace
	OS_REGION_NAME=IAD
	OS_TENANT_NAME=your_rackspace_cloud_username
	OS_USERNAME=your_rackspace_cloud_username
	OS_PASSWORD=your_rackspace_api_key
	OS_PROJECT_ID=your_rackspace_cloud_account_number

    [ord]
	OS_AUTH_URL=https://identity.api.rackspacecloud.com/v2.0/
	NOVA_RAX_AUTH=1
	OS_AUTH_SYSTEM=rackspace
	OS_REGION_NAME=ORD
	OS_TENANT_NAME=your_rackspace_cloud_username
	OS_USERNAME=your_rackspace_cloud_username
	OS_PASSWORD=your_rackspace_api_key
	OS_PROJECT_ID=your_rackspace_cloud_account_number


When you use *supernova*, you'll refer to these environments as **iad** and **ord**.  Every environment is specified by its configuration header name.  See the *Usage* section below for some examples.

**Don't know your Rackspace Cloud account number?** Just log into the [control panel](https://mycloud.rackspace.com/) and look for the number next to your username.  You should see it in the top dark grey bar all the way on the right side.

### Usage

    supernova [--debug] [--list] [environment] [novaclient arguments...]

    Options:
    -h, --help   show this help message and exit
    -d, --debug  show novaclient debug output (overrides NOVACLIENT_DEBUG)
    -l, --list   list all configured environments

##### Passing commands to *nova*

For example, if you wanted to list all instances within the **iad** environment:

    supernova iad list

Show a particular instance's data in the **ord** environment:

    supernova ord show 3edb6dac-5a75-486a-be1b-3b15fd5b4ab0a

The first argument is generally the environment argument and it is expected to be a single word without spaces. Any text after the environment argument is passed directly to *nova*.

##### Debug override

You may optionally pass `--debug` as the first argument (before the environment argument) to see additional debug information about the requests being made to the API:

    supernova --debug iad list

As before, any text after the environment argument is passed directly to *nova*.

##### Listing your configured environments

You can list all of your configured environments by using the `--list` argument.

### Working with keyrings
Due to security policies at certain companies or due to general paranoia, some users may not want API keys or passwords stored in a plaintext *supernova* configuration file.  Luckily, support is now available (via the [keyring](http://pypi.python.org/pypi/keyring) module) for storing any configuration value within your operating system's keychain.  This has been tested on the following platforms:

* Mac: Keychain Access.app
* Linux: gnome-keyring, kwallet (keyring will determine the backend to use based on the system type and configuration. Make sure if you're using linux without Gnome/KDE that you have pycrypto and simplejson/json installed so CryptedFileKeyring is supported or you end up with UncryptedFileKeyring and your keyring won't be encrypted)

To get started, you'll need to choose an environment and a configuration option.  Here's an example of some data you might not want to keep in plain text:

    supernova-keyring --set iad OS_PASSWORD

**TIP**: If you need to use the same data for multiple environments, you can use a global credential item very easily:

    supernova-keyring --set global MyCompanySSO

Once it's stored, you can test a retrieval:

    # Normal, per-environment storage
    supernova-keyring --get production OS_PASSWORD

    # Global storage
    supernova-keyring --get global MyCompanySSO

You'll need to confirm that you want the data from your keychain displayed in plain text (to hopefully thwart shoulder surfers).

Once you've stored your sensitive data, simply adjust your *supernova* configuration file:

    #OS_PASSWORD = really_sensitive_api_key_here
    
    # If using storage per environment
    OS_PASSWORD = USE_KEYRING
    
    # If using global storage
    OS_PASSWORD = USE_KEYRING['MyCompanySSO']

When *supernova* reads your configuration file and spots a value of `USE_KEYRING`, it will look for credentials stored under `OS_PASSWORD` for that environment automatically.  If your keyring doesn't have a corresponding credential, you'll get an exception.

#### A brief note about environment variables

*supernova* will only replace and/or append environment variables to the already present variables for the duration of the *nova* execution. If you have `OS_USERNAME` set outside the script, it won't be used in the script since the script will pull data from `~/.supernova` and use it to run *nova*. In addition, any variables which are set prior to running *supernova* will be left unaltered when the script exits.
