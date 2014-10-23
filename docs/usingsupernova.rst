Using supernova
===============

Passing commands to nova
------------------------

The structure of a supernova command is relatively simple::

    supernova [enviromment_name] [commands]

Here are some examples:

* Listing instances in the *iad* environment::

    supernova iad list

* Listing available images::

    supernova iad image-list

* Listing available flavors::

    supernova iad flavor-list

* Booting an instance::

    supernova iad boot --image image_uuid --flavor flavor_id myserver.example.com

You can use supernova with long-running options and the output will be piped live to your terminal.  For example, you can use ``--poll`` when you boot an instance and you'll see the novaclient output update as your instance is being built.

For debug output, supernova accepts ``--debug`` as a supernova option or as a novaclient option.  Both of these are okay::

    supernova --debug iad list
    supernova iad list --debug

Listing available supernova environments
----------------------------------------

There's a convenience function provided that will dump out your parsed supernova configuration file to the screen::

    supernova -l

This is a good way to test your configuration file syntax and diagnose problems.  Keep in mind that any plain text credentials will be displayed on screen when you list environments (see :ref:`keyring` for more details).

If you're still using plain text credentials, now is a good time to stop using them. :)

Grouped environments
--------------------

Starting in supernova 0.9.6, you can "group" environments and run commands across all of the environments in a group.  Using the `Rackspace example configuration <http://bit.ly/raxsupernova>`_, we can group the DFW, IAD and ORD environments into a group called "raxusa"::

    [dfw]
    SUPERNOVA_GROUP=raxusa
    ...snip...

    [ord]
    SUPERNOVA_GROUP=raxusa
    ...snip...

    [iad]
    SUPERNOVA_GROUP=raxusa
    ...snip...

Instead of referring to these environments one by one, you can now run commands across them as a group::

    supernova raxusa list

This can be quite useful if you need to search multiple environments for an instance, or if you need to boot test instances in multiple datacenters.  Just be careful with any actions that manipulate data, like rebuilds or instance deletions.

Using supernova with different executables
------------------------------------------

While supernova uses the nova executable by default, you can configure it to use any other executable when it runs.  For example, you could use it to run glance, neutron, or keystone.

You can use the same executable for certain environments every time by adding *OS_EXECUTABLE* to your supernova configuration file::

    [iadglance]
    OS_EXECUTABLE=glance
    ...snip...

If you'd rather make a quick change at runtime, just use ``-x`` or ``--executable``::

    supernova -x glance iadglance image-list

Checking the supernova version
------------------------------

As of supernova 1.0.5, you can use the ``--version`` argument to have supernova's version printed on the command line::

    $ supernova --version
    supernova 1.0.5



