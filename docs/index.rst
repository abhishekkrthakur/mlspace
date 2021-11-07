.. mlspace documentation master file, created by
   sphinx-quickstart on Sun Nov  7 15:58:13 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to MLSpace!
===================================

MLSpace is a no-hassle tool for data science, machine learning and deep learning.

MLSpace has pre-made environments for pytorch, tensorflow and everything else you might need.
All environments come with VSCode (code-server) and JupyterLab. You no longer need to care about CUDA/cuDNN versions!

Setting up MLSpace is a three step process:
   - installation
   - set up
   - create and run environments

.. code-block:: bash
   $ mlspace --help

   usage: mlspace <command> [<args>]

   positional arguments:
   {create,setup,start,stop}
                           commands
      create              Create a new MLSpace
      setup               Setup MLSpace and install all dependencies. Run with `sudo`
      start               Start a new space
      stop                Stop a running MLSpace instance

   optional arguments:
   -h, --help            show this help message and exit
   --version, -v         Display MLSpace version

   For more information about a command, run: `mlspace <command> --help`

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   setting_up
   creating_env
   running_env
