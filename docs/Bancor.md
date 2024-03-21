# Bancor Protocol Integration

This repository contains Python code for interacting with the Bancor Protocol, allowing users to fetch data related to liquidity pools and token balances. Below is a brief overview of the provided functionalities and how to use them.

## Contents

- [Bancor Protocol Integration](#bancor-protocol-integration)
  - [Contents](#contents)
  - [Overview](#overview)
  - [Usage](#usage)
    - [Fetching Balance of a Specific Token](#fetching-balance-of-a-specific-token)
    - [Fetching Balances of All Liquidity Pools](#fetching-balances-of-all-liquidity-pools)
  - [Contract Reference](#contract-reference)
  - [Bancor Code Location](#bancor-code-location)

## Overview

The provided Python modules offer functionality to interact with Bancor Protocol's contracts deployed on various blockchains. Key features include:

- Fetching balance of a specific token in a liquidity pool.
- Retrieving balances of all liquidity pools associated with a wallet.

## Usage

### Fetching Balance of a Specific Token

To fetch the balance of a specific token in a liquidity pool, you can use the `get_protocol_data_for` function. Below is an example code snippet demonstrating its usage:

```python
from defyes.protocols.bancor import get_protocol_data_for

# Parameters
token = "<token_address>"
wallet = "<wallet_address>"
blockchain = "<blockchain_name>"
block = "latest"  # or specify a block number or 'latest' for the latest block
reward = True  # Set to True to include reward token balance, False otherwise

# Fetch balance
balances = get_protocol_data_for(token, wallet, blockchain, block, reward)

# Display balances
print("Balances:", balances)
```

### Fetching Balances of All Liquidity Pools

To retrieve balances of all liquidity pools associated with a wallet, you can use the `get_protocol_data` function. Here's how to use it:

```python
from defyes.protocols.bancor import get_protocol_data

# Parameters
blockchain = "<blockchain_name>"
wallet = "<wallet_address>"
block = "latest"  # or specify a block number or 'latest' for the latest block
reward = False  # Set to True to include reward token balance, False otherwise

# Fetch balances
protocol_data = get_protocol_data(blockchain, wallet, block, reward)

# Display protocol data
print("Protocol Data:", protocol_data)
```

Make sure to replace placeholder values (`<token_address>`, `<wallet_address>`, `<blockchain_name>`) with actual values specific to your use case.

## Contract Reference

For detailed information about Bancor Protocol's contracts, refer to the [official developer guides](https://docs.bancor.network/developer-guides/contracts).

## Bancor Code Location

The Bancor Protocol code is located in the following directory within this repository: `defyes/defyes/protocols/bancor`.