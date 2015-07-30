# Getting Started?

Most of the clients produced for OpenStack applications rely on environment variables.  Although environment variables are easy to set and unset, they can become difficult to manage for users that work with more than one endpoint at a time.  This can lead to confusion and that can lead to problems.


## A short anecdote
As an example, I was working with multiple regions of an internal OpenStack cloud at work.  I was migrating some systems from one region to another and deleting the old systems once the new ones were online and running.  Multiple terminals were up on my screen and I was moving along.

Suddenly, monitoring alerts rushed in for a critical system and I couldn't reach it via ssh.  I looked back over my terminals to see what I'd done and I issued the right command in the wrong terminal.  It wasn't entirely obvious which terminal was which unless I took a good look at the environment variables.

## supernova's value

  * **Fewer errors.** Environments must be specified for each supernova run.  This forces you to be deliberate with your choices.
  * **Easier automation.** supernova works well with automated systems, like Jenkins, Ansible, or other scripts.  There's no need to worry about clearing environment variables or setting them on each run.
  * **Flexible.** You can use any OpenStack client along with supernova, like glance, trove, and others.
  * **Non-disruptive.** Nothing in your terminal's environment is changed when supernova runs.  A subprocess is spawned, environment variables are set in the subprocess, and then the entire mess is cleaned up for you, instantly.
  * **Secure.** You can store any configuration item from your OpenStack executable's environment variables in your system's keyring.  This is really handy for usernames, API keys, and passwords.  There's no more risk of leaving a plaintext password laying around on your disks.

## How does supernova work?

### Configuration files
It all starts with a configuration file (see the [Configuration](configuring.md) section for more).  your configuration file has multiple environments (OpenStack endpoints) and configuration items for each environment.  A typical configuration section for one endpoint would look like this:

```html
[production]
OS_AUTH_URL=https://identity.api.rackspacecloud.com/v2.0/
OS_AUTH_SYSTEM=rackspace
OS_COMPUTE_API_VERSION=1.1
NOVA_RAX_AUTH=1
OS_REGION_NAME=DFW
NOVA_SERVICE_NAME=cloudServersOpenStack
OS_PASSWORD=my_password
OS_USERNAME=my_username
OS_TENANT_NAME=my_tenant_name
```

If you want to list all of your instances in the *production* environment with supernova and novaclient, just run one command:

    supernova production list

Simply add another configuration section to your configuration file and change *production* to the name of the second environment to use that one.

### Secure storage
Of course, it's highly recommended to use keyrings for storing your credentials.  That's discussed on the [Configuration](configuring.md) page of the documentation.

### Ready to go
When you run supernova, it parses your configuration file and looks for the configuration options associated with the environment you specified.  If you specified a supernova group (more on that in [Usage](usingsupernova.md)), it will find all of the matching environments and run the executable against them one by one.

If any of those configuration items call for a password from the keyring storage, supernova will retrieve those from your system's keyring and store them in environment variables that will only be made available to the subprocess that supernova will spawn.

At this point, supernova ensures that all arguments to nova are in order and any extra features (like bypass URL's) are configured.

Once all of the arguments, options, and environment variables are assembled, supernova runs the executable you specified (which is nova by default) in a subprocess.  All stdout output will be streamed live to the console and stderr output will be held and then printed once the command has completed.  Once the subprocess exits, all of the environment variables are discarded and you're ready to run a new command.
