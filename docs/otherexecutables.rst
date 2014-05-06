Using supernova with different executables
==========================================

While supernova uses the nova executable by default, you can configure it to use any other executable when it runs.  For example, you could use it to run glance, neutron, or keystone.

You can use the same executable for certain environments every time by adding *OS_EXECUTABLE** to your supernova configuration file:::

    [iadglance]
    OS_EXECUTABLE=glance
    ...snip...

If you'd rather make a quick change at runtime, just use ``-x`` or ``--executable``:::

    supernova -x glance iadglance image-list