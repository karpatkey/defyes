Add a new protocol
================== 

To define a new protocol, it is recommended to create a folder with a meaningful name, such as `mynewprotocol`,
instead of just a Python module like `mynewprotocol.py`. The folder structure should follow this convention:

.. code-block:: text

        protocols/                    # current folder
            mynewprotocol/              # An arbitrary name for the protocol
                __init__.py               # at least empty to make mynewprotocol a python package
                abis/                     # ABIs folder
                    my_abi_definition.json  # An arbitrary name for the ABI.
                    ...                     # more ABI definitions
                autogen_config.json

``mynewprotocol`` is just an example.

After running the command ``make autogenerate``, a file named ``protocols/mynewprotocol/autogenerated.py`` will be generated.
This file contains class definitions for each ABI, with method names converted to snake case. 
Python properties are defined for methods that do not have arguments, for simplicity.

If you prefer not to use the ``make`` command, there's an alternative way to generate the necessary files. You can directly invoke the Python script responsible for this task. Inside the container, execute the following command:

.. code-block:: bash

   python defyes/autogenerate.py

This command will run the `autogenerate.py` script located in the `defyes` directory, performing the same operations as the ``make`` command.


autogen_config.json schema
--------------------------

.. code-block:: json

        {
            "my_abi_definition": {  /* The same name as the .json file you want to be included in autogeneration */
                "const_call": [  /* optional if you want to define some method results as invariant with respect to block_ids */
                    "abiMethodNameAsItIs",
                    /* ... more method names */
                ],
            /* ... more ABI definitions */
        }

__init__.py
-----------

Don't modify ``autogenerated.py``. Instead import the defined classes inside ``autogenerated.py`` into ``__init__.py``, like
this example:

.. code-block:: python

        from .autogenerated import Oracle, Treasury, VaultManager

        # Optionally
        class Oracle(Oracle):
                ...

Optionally you could override the contract class with the same name in this namespace, in order to add for example new high-level
methods or properties, or to override some original methods to change their behaviors. In this example, ``Oracle`` is a
new class in this module's namespace which inherits all the attributes from ``.autogenerated.Oracle``. It won't change the
original ``.autogenerated.Oracle`` behaviors.
