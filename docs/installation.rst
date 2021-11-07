Installation
===================================

There are multiple ways to install MLSpace. Easiest is if you have `python` and `pip` installed.

If you already have `python` & `pip` installed on your system, you can just do:


.. code-block:: bash

    $ pip install -U mlspace


If you do not have `python` and `pip` installed on your system, the first step would be to install them.

.. code-block:: bash

    $ sudo apt-get update
    $ sudo apt-get install -y python3 python3-pip

If you have multiple versions of python installed, you might want to update alternatives and point `python` 
command to a particular version.


.. code-block:: bash
    $ sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 1
    $ sudo update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1


NOTE: MLSpace will work with any python >= 3.5!

Once `python` & `pip` are installed, you can now install `mlspace` using:


.. code-block:: bash

    $ pip install -U mlspace