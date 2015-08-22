# Configuring supernova

The following locations are valid configuration files for supernova.

  * ${XDG_CONFIG_HOME_}/supernova
  * ~/.supernova
  * ./.supernova

Specifying a configuration file manually is also an option:

```html
    supernova -c ~/secrets/supernova_config production list
```

In addition to the nova environment variables the config can include a key of _BYPASS_URL_ that will be passed to nova's --bypass-url command line option.

## Working with keyring storage

With supernova, there are three ways you can store credentials:

  * **Best:** Global keyring storage shared between multiple environments
  * **Better:** Keyring storage specific to an environment
  * **Awful:** Plain text in the supernova configuration file

**NOTE: A temporary environment is spawned by supernova when it actually runs nova -- your credentials aren't left in the environment variables of your current shell.**

Global keyring storage
----------------------

Storing a credential as a global credential allows you to use it across multiple environments.  The greatest benefit of this option is that you only need to set credentials in one place within your keyring.  If you need to change credentials frequently, this can be a big time saver.

Here's how we're already doing that in the [Rackspace example configuration](http://bit.ly/raxsupernova)

    [dfw]
    ... snip ...
    OS_PASSWORD=USE_KEYRING['RackspaceAccountAPIKey']

    [ord]
    ... snip ...
    OS_PASSWORD=USE_KEYRING['RackspaceAccountAPIKey']

    [iad]
    ... snip ...
    OS_PASSWORD=USE_KEYRING['RackspaceAccountAPIKey']

You can set global credentials with supernova-keyring:

    supernova-keyring -s global RackspaceAccountAPIKey

Retrieving a credential you stored previously is easy as well:

    supernova-keyring -g global RackspaceAccountAPIKey

**WARNING:** Retrieving a credential will display it on the screen in plain text.  Someone could shoulder-surf and see your credentials.  Don't worry: supernova will warn you thoroughly before you try this.

# Environment-specific keyring storage

An older method of storing keyring data is to store it specifically for one environment.  Using the [Rackspace example configuration](http://bit.ly/raxsupernova), your DFW configuration might look like this:

    [dfw]
    ... snip ...
    OS_PASSWORD=USE_KEYRING
    OS_USERNAME=my_username
    OS_TENANT_NAME=my_account_number

This tells supernova to look up the *OS_PASSWORD* value for the *dfw* environment.  Setting that credential is done with supernova-keyring:

    supernova-keyring -s dfw OS_PASSWORD

This was one of the first methods of keyring storage available in supernova and it's the least robust.  It's recommended to consider using global keyring storage instead.

# Plain text storage

This is obviously the easiest method, but it's generally not recommended.  Any user with access to your home directory would have access to your credentials and could use them against your accounts.  **Don't use plain text credential storage unless you know what you're doing.**

Using the [Rackspace example configuration](http://bit.ly/raxsupernova), plain text credential storage would look like this::

    [dfw]
    OS_AUTH_URL=https://identity.api.rackspacecloud.com/v2.0/
    OS_AUTH_SYSTEM=rackspace
    OS_COMPUTE_API_VERSION=1.1
    NOVA_RAX_AUTH=1
    OS_REGION_NAME=DFW
    NOVA_SERVICE_NAME=cloudServersOpenStack
    OS_PASSWORD=482aa30919030cafc08f2d2bda2193bf
    OS_USERNAME=my_username
    OS_TENANT_NAME=123456

When supernova runs, it will take the configuration options and pass them directly to nova (or the executable of your choice) in a subprocess.

# Dynamic Configuration

For accounts where you would like to utilize the same configuration, it is possible to use the same entry.

In the configuration, you can separate the regions by a semicolon::

    [personal]
    ..snip..
    OS_REGION_NAME=DFW;ORD
    OS_TENANT_NAME=123456
    OS_USERNAME=username
    OS_PASSWORD=somelongapikey


This will create the super group "personal" as well as the individual groups "personal-DFW" and "personal-ORD"::

    > supernova -l | grep personal
    -- personal-DFW -------------------------------------------------------------
      SUPERNOVA_GROUP      : personal
    -- personal-ORD -------------------------------------------------------------
      SUPERNOVA_GROUP      : personal
