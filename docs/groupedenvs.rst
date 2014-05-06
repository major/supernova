Grouped environments
====================

Starting in supernova 0.9.6, you can "group" environments and run commands across all of the environments in a group.  Using the `Rackspace example configuration <http://bit.ly/raxsupernova>`_, we can group the DFW, IAD and ORD environments into a group called "raxusa":::

    [dfw]
    SUPERNOVA_GROUP=raxusa
    ...snip...

    [ord]
    SUPERNOVA_GROUP=raxusa
    ...snip...

    [iad]
    SUPERNOVA_GROUP=raxusa
    ...snip...

Instead of referring to these environments one by one, you can now run commands across them as a group:::

    supernova raxusa list

This can be quite useful if you need to search multiple environments for an instance, or if you need to boot test instances in multiple datacenters.  Just be careful with any actions that manipulate data, like rebuilds or instance deletions.