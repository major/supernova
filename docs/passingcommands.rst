Passing commands to nova
========================

The structure of a supernova command is relatively simple:::

    supernova [enviromment_name] [commands]

Here are some examples:

* Listing instances in the *iad* environment:::

    supernova iad list

* Listing available images:::

    supernova iad image-list

* Listing available flavors:::

    supernova iad flavor-list

* Booting an instance:::

    supernova iad boot --image image_uuid --flavor flavor_id myserver.example.com

You can use supernova with long-running options and the output will be piped live to your terminal.  For example, you can use ``--poll`` when you boot an instance and you'll see the novaclient output update as your instance is being built.

For debug output, supernova accepts ``--debug`` as a supernova option or as a novaclient option.  Both of these are okay:::

    supernova --debug iad list
    supernova iad list --debug