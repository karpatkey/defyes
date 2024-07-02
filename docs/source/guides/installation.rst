Installation and Setup
======================

Install
-------

When using ``defyes`` as a library, you have two ways to install it:

.. code-block:: bash

   pip install . 'defyes[all]'

or, if you experiment dependencies conflicts, you can take control over some dependencies version by removing ``[all]``
but specifying each missing dependency.

.. code-block:: bash

   pip install . 'defyes'
   pip install "karpatkit @ git+https://github.com/karpatkey/karpatkit.git@another_specific_version"

where ``another_specific_version`` should be a git reference (tag, hash, branch).

Have a look at ``all`` in the `pyproject.toml <pyproject.toml>`_ file, ``[project.optional-dependencies]`` section.

.. note::

   Take into account that installing just ``defyes`` without ``defyes[all]`` is an incomplete installation.


Configuration
-------------

To successfully configure and run the package, you'll need to set up your RPC endpoints and provide necessary API keys. Follow the steps below to get started:

1. **Copy, Rename, and Modify the Configuration File**
   - You can find the example configuration file `here <https://github.com/karpatkey/defyes/blob/main/example_config.json>`_.
   - Modify name and info in this file to include your specific RPC endpoints and API keys.

2. **Provide RPC Endpoints and Explorer API Keys**
   - Provide the necessary ``EXPLORER API KEYS`` for accessing various blockchain explorers.
   - The blockchain explorers are used to fetch additional information for a set of functions in the package.

3. **Set the CONFIG_PATH Environment Variable**
   - Set the ``CONFIG_PATH`` environment variable to point to the absolute path of your ``config.json`` file. This allows the package to locate and use your configuration file.

Example Configuration Steps
----------------------------

Here's an example of how to set the ``CONFIG_PATH`` environment variable in a Unix-like terminal (such as Linux or macOS):

.. code-block:: sh

    # Assuming your config.json is located at /path/to/your/config.json
    export CONFIG_PATH=/path/to/your/config.json

