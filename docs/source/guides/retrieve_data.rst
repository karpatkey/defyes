Retrieve Data
=============

Here an example on how to get data from one of the protocols.


Mu example
----------

Here's an example of how to use the ``get_protocol_data_for`` function:

.. code-block:: python

   from defyes.protocols.mu import get_protocol_data_for

   # Define the blockchain, wallet, and position_identifier
   blockchain = 'ethereum'
   wallet = '0xYourWalletAddress'
   position_identifier = '0xVaultAddress'

   # Call the function
   result = get_protocol_data_for(blockchain, wallet, position_identifier)

   # Print the result
   print(result)

In this example, replace `'ethereum'` with the blockchain you're interacting with, `'0xYourWalletAddress'` with the address of your wallet, and `'0xVaultAddress'` with the address of the vault you want to get data from.

Result
------

The function returns a dictionary with the data for the wallet for the mu exchange protocol. The exact structure of the dictionary depends on the data available in the vault at the specified block.

.. note::

   The `block` parameter can be an integer representing a block number, or a string representing a block tag. If not provided, it defaults to `"latest"`, which fetches data from the latest block.

   The `decimals` parameter is a boolean that determines whether to include decimals in the data. If not provided, it defaults to `True`.