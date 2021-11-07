Creating an environment
===================================

An environment can be created using the `mlspace create` command.

For example, you can create a `torch` environment without GPU using:

.. code-block:: bash

    $ mlspace create --name name_of_your_env --backend torch


and if you want to create an environment with GPU support, just add `--gpu` to the create command.


.. code-block:: bash

    $ mlspace create --name name_of_your_env --backend torch --gpu


At any point, you can get help for a command using `--help`. E.g.

.. code-block:: bash

    $ mlspace create --help

    usage: mlspace <command> [<args>] create [-h] --name NAME --backend {torch} [--gpu]

    optional arguments:
    -h, --help         show this help message and exit
    --name NAME        Name of MLSpace
    --backend {torch}  MLSpace backend
    --gpu              Whether to use GPU
