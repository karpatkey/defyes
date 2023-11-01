
<!-- logo -->
<p align="center">
  <img width='400' src="https://raw.github.com/KarpatkeyDAO/defyes/main/img/karpatkey_logo_black.png">
</p>

<!-- tag line -->
<h3 align='center'> Python package for Defi Protocols! </h3>

## 🌻 Motivation

 Karpatkey tech team has always been dealing with defi protocols for various purposes, like getting prices, underlying tokens, pools, rewards, alerts, fees, reporting, APRs, etc. As a result of this search we created this protocol with all the knowledge acquired to contribute to the web3 and DEFI community. We hope it will be useful for your developments!


## Repo Url

[KarpatkeyDAO/defyes](https://github.com/KarpatkeyDAO/defyes)


## Installing from repository

```bash
pip3 install git+https://github.com/KarpatkeyDAO/defyes.git
```

## Installing latest version available on pypi

[pip3 install defyes](https://pypi.org/project/defyes/)


## Config 

- First you will have to modify the [config.json](https://github.com/KarpatkeyDAO/defyes/blob/main/defyes/config.json)

- You should provide `RPC` endpoints and `EXPLORER API KEYS`

- You should set the env `CONFIG_PATH` env with the config.json's absolute path or the config.json can be placed under default package path `/path/to/python/site-packages/defyes/config.json`

  <details><summary><b>Test</b></summary>

  ```bash
  nano /tmp/config.json

  export CONFIG_PATH=/tmp/config.json
  ```
  ```python
  from defyes.constants import config_data

  print(config_data)
  ```

  ```bash
  output: 
  {'apikeys': {'etherscan': 'xyz', 'polscan': 'xyz', 'gnosisscan': 'xyz', 'binance': 'xyz', 'avalanche': 'xyz', 'fantom': 'xyz', 'ethplorer': 'xyz'}, 'nodes': {'ethereum': {'latest': ['first', 'second', 'third', 'fourth'], 'archival': ['first', 'second', 'third', 'fourth']}, 'polygon': {'latest': ['first', 'second', 'third', 'fourth'], 'archival': ['first', 'second', 'third', 'fourth']}, 'xdai': {'latest': ['first', 'second', 'third', 'fourth'], 'archival': ['first', 'second', 'third', 'fourth']}, 'binance': {'latest': ['first', 'second', 'third', 'fourth'], 'archival': ['first', 'second', 'third', 'fourth']}, 'avalanche': {'latest': ['first', 'second', 'third', 'fourth'], 'archival': ['first', 'second', 'third', 'fourth']}, 'fantom': {'latest': ['first', 'second', 'third', 'fourth'], 'archival': ['first', 'second', 'third', 'fourth']}, 'ropsten': {'latest': ['first', 'second', 'third', 'fourth'], 'archival': ['first', 'second', 'third', 'fourth']}, 'kovan': {'latest': ['first', 'second', 'third', 'fourth'], 'archival': ['first', 'second', 'third', 'fourth']}, 'goerli': {'latest': ['first', 'second', 'third', 'fourth'], 'archival': ['first', 'second', 'third', 'fourth']}}}
  ```

  </details>

## Protocols supported


| Protocol      | Underlying | Rewards | Fees | docs |
|---------------|------------|---------|------|------|
| AAVE          | ✔          | ✔       |  -   |  [link](https://github.com/KarpatkeyDAO/defyes/blob/main/docs/Aave.md)   |
| Agave         | ✔          | ✔       |  -   |  [link](https://github.com/KarpatkeyDAO/defyes/blob/main/docs/Agave.md)   |
| Aura          | ✔          | ✔       |  -   |  [link](https://github.com/KarpatkeyDAO/defyes/blob/main/docs/Aura.md)   |
| Balancer      | ✔          | ✔       |  ✔   |  [link](https://github.com/KarpatkeyDAO/defyes/blob/main/docs/Balancer.md)   |
| Bancor        | ✔          | ?       |  -   |  [link](https://github.com/KarpatkeyDAO/defyes/blob/main/docs/Bancor.md)   |
| Compound      | ✔          | pending |  -   |  [link](https://github.com/KarpatkeyDAO/defyes/blob/main/docs/Compound.md)   |
| Convex        | ✔          | ✔       |  -   |  [link](https://github.com/KarpatkeyDAO/defyes/blob/main/docs/Convex.md)   |
| Curve         | ✔          | ✔       |  ✔   |  [link](https://github.com/KarpatkeyDAO/defyes/blob/main/docs/Curve.md)   |
| Elk           | ✔          | ✔       |  ✔   |  [link](https://github.com/KarpatkeyDAO/defyes/blob/main/docs/Elk.md)   |
| Honeyswap     | ✔          | -       |  ✔   |  [link](https://github.com/KarpatkeyDAO/defyes/blob/main/docs/Honeyswap.md)   |
| Maker         | ✔          | -       |  -   |  [link](https://github.com/KarpatkeyDAO/defyes/blob/main/docs/Maker.md)   |
| QiDao         | ✔          | -       |  -   |  [link](https://github.com/KarpatkeyDAO/defyes/blob/main/docs/QiDao.md)   |
| SushiSwap     | ✔          | ✔       |  ✔   |  [link](https://github.com/KarpatkeyDAO/defyes/blob/main/docs/Sushiswap.md)   |
| Swapr         | ✔          | ✔       |  ✔   |  [link](https://github.com/KarpatkeyDAO/defyes/blob/main/docs/Swapr.md)   |
| Symmetric     | ✔          | ✔       |  ✔   |  [link](https://github.com/KarpatkeyDAO/defyes/blob/main/docs/Symmetric.md)   |
| Unit Protocol | ✔          | ✔       |  -   |  [link](https://github.com/KarpatkeyDAO/defyes/blob/main/docs/Unit.md)   |
| Uniswap V3    | ✔          | ?       |  -   |  [link](https://github.com/KarpatkeyDAO/defyes/blob/main/docs/UniswapV3.md)   |

## Cache

To reduce the number of calls to RPC endpoints, and thus significantly speed up the functions, defyes implements a cache where the result of some web3 calls are stored.
If the same web3 function is called, with the very same arguments, its result will be retrieved from the cache.

By default the cache is enabled and caches all calls to web3 'eth_call' when a block other than 'latest' is specified.
In practice this means that the following example calls will be cached:

    ```python
    chef_contract.functions.totalAllocPoint().call(block_identifier=1560000)

    chef_contract.functions.poolLength().call(block_identifier=block)

    token_contract.functions.decimals().call(block_identifier=block)
    ```

The following calls will not be cached:

    ```python
    chef_contract.functions.poolLength().call(block_identifier='latest')

    token_contract.functions.decimals().call()

    web3.eth.get_balance()

    contract.functions.updateValue(43).transact()

    ```

This functionality of the cache is very useful as long as the same block can be used, even if only for a while, since successive calls will bring the responses from the cache. This is very useful for example in tests or when developing.

There are some calls that are expected to always return the same value from the blockchain.
For example, `token.contract.decimals.call(block_identifier=block)`, will return the same value if the block is equal or greater than the block the contract was deployed.
For this type of calls, which return something constant in time, the automatic cache is  not useful because if a block is specified, the value will only be used for that block. And if 'latest' is specified, it is automatically excluded from the cache.
For these cases the const_call() helper function is used.

### `const_call()` helper

The `const_call()` function forces the caching of a `.call()` without defining a block. Thus subsequent calls to `const_call()` will return the same result even if the block is different from the block in which the result was cached.
Warning: if a call is made after caching using a block prior to the contract creation, `const_call()` will reuse the locally stored value instead of returning an error.

Example usage:

    ```
    const_call(token_contract.functions.decimals())

    const_call(pool_contract.functions.token0())
    ```

### Cache config

By default the cache is stored in a non persistent directory `/tmp/defyes/`.
To change the directory use the environment variable `DEFI_PROTO_CACHE_DIR=/path/to/dir`.

To disable the cache define the `DEFI_PROTO_CACHE_DISABLE` environment variable.

To wipe the cache use the env var `DEFI_PROTO_CACHE_CLEAR` or call `defyes.cache.clear()`.


## Docs

- <details><summary><b>Functions</b></summary>

  # Functions

  ## Defined in functions.py


  ### 1: get_node(blockchain, block='latest')

  > Description: function returns web3 object of the node

  - <details><summary><b>Example</b></summary>

    ```
    a = get_node(Chain.ETHEREUM, 'latest')
    print(a)
    ```

    ```
    output:
    <web3.main.Web3 object at 0x7fe8c584b8b0>
    ```
    </details>

  ### 2: last_block(blockchain, web3=None, block='latest')

  > Description: functoion returns last block of the blockchain

  - <details><summary><b>Example</b></summary>

    ```
    a = last_block(Chain.ETHEREUM, None, 'latest')
    print(a)
    ```

    ```
    output:
    16370420
    ```
    </details>

  ### 6: date_to_block(datestring, blockchain) -> int

  > Description: function returns date to block conversion

  - <details><summary><b>Example</b></summary>

    ```bash
    a = date_to_block('2022-01-14 00:00:00', Chain.ETHEREUM)
    print(a)

    ```

    ```
    output:
    14000270
    ```
    </details>

  ### 8: block_to_date(block, blockchain)

  > Description: function returns block to date conversion

  - <details><summary><b>Example</b></summary>

    ```bash
    a = block_to_date(14000270, Chain.ETHEREUM)
    print(a)

    ```

    ```
    output:
    2022-01-13 23:59:54
    ```
    </details>

  ### 9: get_blocks_per_year(blockchain)

  > Description: function returns blocks per year for a blockchain

  - <details><summary><b>Example</b></summary>

    ```bash
    a = get_blocks_per_year(Chain.ETHEREUM)
    print(a)

    ```

    ```
    output:
    2398217
    ```
    </details>

  ### 10: token_info(token_address, blockchain)

  > Description: function returns token related info

  - <details><summary><b>Example</b></summary>

    ```bash
    a = token_info('0x6810e776880C02933D47DB1b9fc05908e5386b96', Chain.ETHEREUM)
    print (a)

    ```

    ```
    output:
    {'address': '0x6810e776880c02933d47db1b9fc05908e5386b96', 'name': 'Gnosis', 'decimals': '18', 'symbol': 'GNO', 'totalSupply': '10000000000000000000000000', 'owner': '', 'txsCount': 154486, 'transfersCount': 318423, 'lastUpdated': 1673304547, 'issuancesCount': 0, 'holdersCount': 16650, 'website': 'https://gnosis.pm/', 'image': '/images/GNO6810e776.png', 'ethTransfersCount': 0, 'price': {'rate': 91.2045572764551, 'diff': 4, 'diff7d': 8.78, 'ts': 1673304180, 'marketCapUsd': 236182227.06842083, 'availableSupply': 2589588, 'volume24h': 1954362.90295114, 'volDiff1': 17.234718455656363, 'volDiff7': 1358.516624011187, 'volDiff30': 108.75660649607727, 'diff30d': 1.367903603382814, 'bid': 323.4, 'currency': 'USD'}, 'publicTags': ['DEX', 'Protocol', 'DeFi'], 'countOps': 318423}
    ```
    </details>

  ### 11: balance_of(address, contract_address, block, blockchain, execution=1, web3=None, index=0, decimals=True)

  > Description: function returns ballance of given wallet for given contract

  - <details><summary><b>Example</b></summary>

    ```bash
    a = balance_of('0x2D0669DB84f11A9EAD41e57Ce2f242D92111a58F', '0x6810e776880C02933D47DB1b9fc05908e5386b96', 'latest', Chain.ETHEREUM)
    print(a)

    ```

    ```
    output:
    0.0
    ```
    </details>

  ### 12: total_supply(token_address, block, blockchain, execution=1, web3=None, index=0, decimals=True)

  > Description: function returns total suppy for a given token contract address

  - <details><summary><b>Example</b></summary>

    ```bash
    a = total_supply('0x6810e776880C02933D47DB1b9fc05908e5386b96', 'latest', Chain.ETHEREUM)
    print(a)

    ```

    ```
    output:
    10000000.0
    ```
    </details>

  ### 13: get_decimals(token_address, blockchain, execution=1, web3=None, block='latest')

  > Description: function returns decimals for given token address


  ### 14: get_symbol(token_address, blockchain, execution=1, web3=None, block='latest', index=0) -> str

  > Description: function returns symbol for given toke contract address

  ### 15: get_contract_abi(contract_address, blockchain)

  > function returns abi for given contract address

  ### 16: get_contract(contract_address, blockchain, web3=None, abi=None, block='latest', index=0)

  > Description: function returns web3 contract object for given contract object

  - <details><summary><b>Example</b></summary>

    ```bash
    print(get_contract('0xdAC17F958D2ee523a2206206994597C13D831ec7', Chain.ETHEREUM))

    ```

    ```
    output:
    <web3._utils.datatypes.Contract object at 0x7f1dfdcb7af0>
    ```
    </details>

  ### 16: get_contract_proxy_abi(contract_address, abi_contract_address, blockchain, web3=None, block='latest', index=0)

  > Description: function returns abi for given contract with the help of proxy conract

  - <details><summary><b>Example</b></summary>

    ```bash
    # a = get_contract_abi('0xdc31ee1784292379fbb2964b3b9c4124d8f89c60', Chain.GOERLI)

    # print(a)

    b = get_contract_proxy_abi('0xdc31ee1784292379fbb2964b3b9c4124d8f89c60', '0xe2E52C2D0D64209b8DD1854371A4C673c13448f0', Chain.GOERLI)

    print(b)
    ```

    ```
    output:
    <web3._utils.datatypes.Contract object at 0x7f61efe07af0>
    ```
    </details>

  ### 17: search_proxy_contract(contract_address, blockchain, web3=None)

  > Description: function returns proxy contracts for given contract

  - <details><summary><b>Example</b></summary>

    ```bash
    d = search_proxy_contract('0x4aa42145Aa6Ebf72e164C9bBC74fbD3788045016', Chain.GNOSIS)

    print(d)

    ```

    ```
    output:
    <web3._utils.datatypes.Contract object at 0x7f0ac475ba90>
    ```
    </details>

  ### 18: get_abi_function_signatures(contract_address, blockchain, web3=None, abi_address=None)

  > Description: function returns function signatures for givenn contract address

  - <details><summary><b>Example</b></summary>

    ```bash
    d = get_abi_function_signatures('0x4aa42145Aa6Ebf72e164C9bBC74fbD3788045016', Chain.GNOSIS)

    print(d)

    ```

    ```
    output:
    [{'name': 'claimValues', 'signature': 'claimValues(address,address)', 'inline_signature': 'claimValues(address,address)', 'components': ['address', 'address'], 'stateMutability': 'nonpayable'}, {'name': 'owner', 'signature': 'owner()', 'inline_signature': 'owner()', 'components': [], 'stateMutability': 'view'}, {'name': 'transferOwnership', 'signature': 'transferOwnership(address)', 'inline_signature': 'transferOwnership(address)', 'components': ['address'], 'stateMutability': 'nonpayable'}]
    ```
    </details>

  ### 19: get_data(contract_address, function_name, parameters, blockchain, web3=None, abi_address=None)

  > Description: function returns data of a specific function of given contract address

  - <details><summary><b>Example</b></summary>

    ```bash
    d = get_data('0x4aa42145Aa6Ebf72e164C9bBC74fbD3788045016', 'owner', None, Chain.GNOSIS)

    print(d)

    ```

    ```
    output:
    0x8da5cb5b
    ```
    </details>

  ### 20: get_token_tx(token_address, contract_address, block_start, block_end, blockchain)

  > Description: function returns transactions on given contract for given token address for given block range

  - <details><summary><b>Example</b></summary>

    ```bash
    e = get_token_tx('0x4ECaBa5870353805a9F068101A40E0f32ed605C6', '0xc30141B657f4216252dc59Af2e7CdB9D8792e1B0', 25813406, 'latest', Chain.GNOSIS)

    print(e)

    ```

    ```
    output:
    [{'blockNumber': '25848427', 'timeStamp': '1673114785', 'hash': '0x75a397e95e3e5761b21f05ead73834455fda37888ec27079a8f1a45b24b6d1cb', 'nonce': '686', 'blockHash': '0x7f818d65d54f4a00ae968965a13d5d7cd113b67f0fba326d674cefa3ec8bb2b6', 'from': '0xc30141b657f4216252dc59af2e7cdb9d8792e1b0', 'contractAddress': '0x4ecaba5870353805a9f068101a40e0f32ed605c6', 'to': '0xac313d7491910516e06fbfc2a0b5bb49bb072d91', 'value': '101454525', 'tokenName': 'Tether USD on xDai', 'tokenSymbol': 'USDT', 'tokenDecimal': '6', 'transactionIndex': '1', 'gas': '926025', 'gasPrice': '1825346000', 'gasUsed': '562326', 'cumulativeGasUsed': '583326', 'input': 'deprecated', 'confirmations': '36987'}, {'blockNumber': '25848427', 'timeStamp': '1673114785', 'hash': '0x75a397e95e3e5761b21f05ead73834455fda37888ec27079a8f1a45b24b6d1cb', 'nonce': '686', 'blockHash': '0x7f818d65d54f4a00ae968965a13d5d7cd113b67f0fba326d674cefa3ec8bb2b6', 'from': '0x1111111254fb6c44bac0bed2854e76f90643097d', 'contractAddress': '0x4ecaba5870353805a9f068101a40e0f32ed605c6', 'to': '0xc30141b657f4216252dc59af2e7cdb9d8792e1b0', 'value': '101454525', 'tokenName': 'Tether USD on xDai', 'tokenSymbol': 'USDT', 'tokenDecimal': '6', 'transactionIndex': '1', 'gas': '926025', 'gasPrice': '1825346000', 'gasUsed': '562326', 'cumulativeGasUsed': '583326', 'input': 'deprecated', 'confirmations': '36987'}, {'blockNumber': '25842520', 'timeStamp': '1673084125', 'hash': '0x521a6ed38b407d3101456135fdae3428e5ce32eb6749ed8bee1beeb28591bb79', 'nonce': '471', 'blockHash': '0x322acd3bad3b462d053e014c088b164c7d17491d683d946d7edb4f7374bc14c4', 'from': '0xc30141b657f4216252dc59af2e7cdb9d8792e1b0', 'contractAddress': '0x4ecaba5870353805a9f068101a40e0f32ed605c6', 'to': '0xac313d7491910516e06fbfc2a0b5bb49bb072d91', 'value': '36272803', 'tokenName': 'Tether USD on xDai', 'tokenSymbol': 'USDT', 'tokenDecimal': '6', 'transactionIndex': '5', 'gas': '828950', 'gasPrice': '2000000007', 'gasUsed': '535324', 'cumulativeGasUsed': '886617', 'input': 'deprecated', 'confirmations': '42894'}, {'blockNumber': '25842520', 'timeStamp': '1673084125', 'hash': '0x521a6ed38b407d3101456135fdae3428e5ce32eb6749ed8bee1beeb28591bb79', 'nonce': '471', 'blockHash': '0x322acd3bad3b462d053e014c088b164c7d17491d683d946d7edb4f7374bc14c4', 'from': '0x1111111254fb6c44bac0bed2854e76f90643097d', 'contractAddress': '0x4ecaba5870353805a9f068101a40e0f32ed605c6', 'to': '0xc30141b657f4216252dc59af2e7cdb9d8792e1b0', 'value': '36272803', 'tokenName': 'Tether USD on xDai', 'tokenSymbol': 'USDT', 'tokenDecimal': '6', 'transactionIndex': '5', 'gas': '828950', 'gasPrice': '2000000007', 'gasUsed': '535324', 'cumulativeGasUsed': '886617', 'input': 'deprecated', 'confirmations': '42894'}, {'blockNumber': '25814478', 'timeStamp': '1672938840', 'hash': '0x48c01f261497eb2ab9a82dfd019d4d019b7d5bd9707399e1ae8ec0891542bf29', 'nonce': '3132', 'blockHash': '0xcb1b78d76b7ca57c8feaff09862662d071a9fefe435e7dc7baf14e5b954ac45b', 'from': '0xc30141b657f4216252dc59af2e7cdb9d8792e1b0', 'contractAddress': '0x4ecaba5870353805a9f068101a40e0f32ed605c6', 'to': '0xac313d7491910516e06fbfc2a0b5bb49bb072d91', 'value': '48987164', 'tokenName': 'Tether USD on xDai', 'tokenSymbol': 'USDT', 'tokenDecimal': '6', 'transactionIndex': '1', 'gas': '1007940', 'gasPrice': '1500000007', 'gasUsed': '610897', 'cumulativeGasUsed': '802730', 'input': 'deprecated', 'confirmations': '70936'}, {'blockNumber': '25814478', 'timeStamp': '1672938840', 'hash': '0x48c01f261497eb2ab9a82dfd019d4d019b7d5bd9707399e1ae8ec0891542bf29', 'nonce': '3132', 'blockHash': '0xcb1b78d76b7ca57c8feaff09862662d071a9fefe435e7dc7baf14e5b954ac45b', 'from': '0x1111111254fb6c44bac0bed2854e76f90643097d', 'contractAddress': '0x4ecaba5870353805a9f068101a40e0f32ed605c6', 'to': '0xc30141b657f4216252dc59af2e7cdb9d8792e1b0', 'value': '48987164', 'tokenName': 'Tether USD on xDai', 'tokenSymbol': 'USDT', 'tokenDecimal': '6', 'transactionIndex': '1', 'gas': '1007940', 'gasPrice': '1500000007', 'gasUsed': '610897', 'cumulativeGasUsed': '802730', 'input': 'deprecated', 'confirmations': '70936'}]
    ```
    </details>

  ### 21: get_tx_list(contract_address, block_start, block_end, blockchain)

  > Description: function returns txs list for given contract address for given block range


  - <details><summary><b>Example</b></summary>

    ```bash
    e = get_tx_list('0x4ECaBa5870353805a9F068101A40E0f32ed605C6', 25884100, 'latest', Chain.GNOSIS)

    print(e)

    ```

    ```
    output:
    [{'blockNumber': '25884304', 'timeStamp': '1673301985', 'hash': '0x2eb63c1d0af69b41969515885badb605a791a1ae4917339d895294ec88b8c4c2', 'nonce': '3', 'blockHash': '0x1f5189238d55e31fd9510022a3a50d0649f5a8110601ed138f4661a1de862460', 'transactionIndex': '41', 'from': '0x10e35f286bc156272c6846b97d1a95b9555ced4b', 'to': '0x4ecaba5870353805a9f068101a40e0f32ed605c6', 'value': '0', 'gas': '289343', 'gasPrice': '2910000001', 'isError': '1', 'txreceipt_status': '0', 'input': '0x4000aea0000000000000000000000000f6a78083ca3e2a662d6dd1703c939c8ace2e268d00000000000000000000000000000000000000000000000000000000124616160000000000000000000000000000000000000000000000000000000000000060000000000000000000000000000000000000000000000000000000000000001410e35f286bc156272c6846b97d1a95b9555ced4b000000000000000000000000', 'contractAddress': '', 'cumulativeGasUsed': '3381775', 'gasUsed': '30207', 'confirmations': '1169', 'methodId': '0x4000aea0', 'functionName': 'transferAndCall(address _to, uint256 _value, bytes _data)'}, {'blockNumber': '25884303', 'timeStamp': '1673301980', 'hash': '0x75b29da1b0ea555d70955ebeacc2797e46f60deb6540805ed68a6585c78f8699', 'nonce': '2', 'blockHash': '0x32044065f599e8c4f4c5fb9ce3e17b0d3633678b10b462e0bd3417a0caaf9636', 'transactionIndex': '0', 'from': '0x10e35f286bc156272c6846b97d1a95b9555ced4b', 'to': '0x4ecaba5870353805a9f068101a40e0f32ed605c6', 'value': '0', 'gas': '289343', 'gasPrice': '2910000001', 'isError': '0', 'txreceipt_status': '1', 'input': '0x4000aea0000000000000000000000000f6a78083ca3e2a662d6dd1703c939c8ace2e268d00000000000000000000000000000000000000000000000000000000124616160000000000000000000000000000000000000000000000000000000000000060000000000000000000000000000000000000000000000000000000000000001410e35f286bc156272c6846b97d1a95b9555ced4b000000000000000000000000', 'contractAddress': '', 'cumulativeGasUsed': '227528', 'gasUsed': '227528', 'confirmations': '1170', 'methodId': '0x4000aea0', 'functionName': 'transferAndCall(address _to, uint256 _value, bytes _data)'}]
    ```
    </details>

  ### 22: get_logs(block_start, block_end, address, topic0, blockchain, **kwargs)

  > Description: function returns logs data for given block range for specified contract/address

  ** Example needed **

  ### 23: is_archival(endpoint) -> bool

  > Description: function returns if node is an archival node or a full node.



  </details>

- <details><summary><b>Logging</b></summary>

  # Logging config

  ## General setup for an application

  defyes will emit several logs using the standard libary logging module. It is expected that the application does the logging setup, for example using `logging.basicConfig`. You can use the standard logger interface to change the log level for defyes’s logger:

  ```python
  import logging
  logging.getLogger("defi_protocol").setLevel(logging.WARNING)
  ```

  ## Quick logging config

  Call `defi_protocol.add_stderr_logger(logging.DEBUG)` to setup a quick logging handler that logs to stderr.

  </details>

- <details><summary><b>Aave</b></summary>

  # Running in a Docker container

  ## Build

  In the repository root path run:
  ```console
  docker build -t <container_name>:<container_tag> .
  ```


  # Aave

  ## Defined in Aave.py


  ### 1: get_reserves_tokens(pdp_contract, block)

  > Description: function returns reserved tokens for aave protocol v2

  - <details><summary><b>Example</b></summary>

    ```
    from defyes.functions import *

    from defyes import Aave

    f1 = get_contract('0x057835Ad21a177dbdd3090bB1CAE03EaCF78Fc6d', Chain.ETHEREUM)

    f2 = Aave.get_reserves_tokens(f1, 'latest')

    print(f2)

    ```

    ```
    output:
    ['0xdAC17F958D2ee523a2206206994597C13D831ec7', '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599', '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', '0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e', '0xE41d2489571d322189246DaFA5ebDe1F4699F498', '0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984', '0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9', '0x0D8775F648430679A709E98d2b0Cb6250d2887EF', '0x4Fabb145d64652a948d72533023f6E7A623C7C53', '0x6B175474E89094C44Da98b954EedeAC495271d0F', '0xF629cBd94d3791C9250152BD8dfBDF380E2a3B9c', '0xdd974D5C2e2928deA5F71b9825b8b646686BD200', '0x514910771AF9Ca656af840dff83E8264EcF986CA', '0x0F5D2fB29fb7d3CFeE444a200298f468908cC942', '0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2', '0x408e41876cCCDC0F92210600ef50372656052a38', '0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F', '0x57Ab1ec28D129707052df4dF418D58a2D46d5f51', '0x0000000000085d4780B73119b644AE5ecd22b376', '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', '0xD533a949740bb3306d119CC777fa900bA034cd52', '0x056Fd409E1d7A124BD7017459dFEa2F387b6d5Cd', '0xba100000625a3754423978a60c9317c58a424e3D', '0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272', '0xD5147bc8e386d91Cc5DBE72099DAC6C9b99276F5', '0x03ab458634910AaD20eF5f1C8ee96F1D6ac54919', '0xD46bA6D942050d489DBd938a2C909A5d5039A161', '0x8E870D67F660D95d5be530380D0eC0bd388289E1', '0x1494CA1F11D487c2bBe4543E90080AeBa4BA3C2b', '0x853d955aCEf822Db058eb8505911ED77F175b99e', '0x956F47F50A910163D8BF957Cf5846D573E7f87CA', '0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84', '0xC18360217D8F7Ab5e7c516566761Ea12Ce7F9D72', '0xa693B19d2931d498c5B318dF961919BB4aee87a5', '0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B', '0x111111111117dC0aa78b770fA6A738034120C302', '0x5f98805A4E8be255a32880FDeC7F6728C6568bA0']
    ```
    </details>

  ### 2: get_reserves_tokens_balances(web3, wallet, block, blockchain, decimals=True)

  > Description: function returns reserved token ballances for given wallet

  - <details><summary><b>Example</b></summary>

    ```
    from defyes.functions import *

    from defyes import Aave

    web3 = get_node(Chain.ETHEREUM, 'latest', 0)

    f2 = Aave.get_reserves_tokens_balances(web3, '0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', Chain.ETHEREUM)

    print(f2)

    ```

    ```
    output: [['0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599', -25.1759987], ['0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84', 1385.4727732126728]]
    
    ```
    </details>

  ### 3: get_data(wallet, block, blockchain, execution = 1, web3=None, index=0, decimals=True)

  > Description: function returns aave protocol data for given wallet

  - <details><summary><b>Example</b></summary>

    ```
    from defyes.functions import *

    from defyes import Aave

    f3 = Aave.get_data('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', Chain.ETHEREUM)

    print(f3)

    ```

    ```
    output: 

    {'collateral_ratio': 422.8517007532872, 'liquidation_ratio': 120.48192771084337, 'eth_price_usd': 1321.28, 'collaterals': [{'token_address': '0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84', 'token_amount': 1385.4727732126728, 'token_price_usd': 1309.82714496}], 'debts': [{'token_address': '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599', 'token_amount': 25.17600199, 'token_price_usd': 17046.574635530906}]}
    
    ```
    </details>


  ### 4: get_all_rewards(wallet, block, blockchain, execution = 1, web3=None, index=0, decimals=True)

  > Description: function returns all the rewards for given wallet from aave protocol

  - <details><summary><b>Example</b></summary>

    ```
    from defyes.functions import *

    from defyes import Aave

    f4 = Aave.get_all_rewards('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', Chain.ETHEREUM)

    print(f4)

    ```

    ```
    output: 

    [['0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9', 5.046433045046507]]
    
    ```

  ### 5: underlying(wallet, block, blockchain, execution=1, web3=None, index=0, decimals=True, reward=False)

  > Description: function returns underlying tokens for given wallter from aave protocol

  - <details><summary><b>Example</b></summary>

    ```
    from defyes.functions import *

    from defyes import Aave

    f5 = Aave.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', Chain.ETHEREUM, reward=True)

    print(f5)

    ```

    ```
    output: 

    [[['0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599', -25.17600614], ['0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84', 1385.4727732126728]], [['0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9', 5.046433045046507]]]
    
    ```
    
  </details>


- <details><summary><b>Agave</b></summary>

  # Agave

  ## Defined in Agave.py


  ### 1: get_reserves_tokens(pdp_contract, block)

  > Description: function returns reserved tokens for agave protocol

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Agave


    f1 = Agave.get_contract('0x24dCbd376Db23e4771375092344f5CbEA3541FC0', Chain.GNOSIS)
    f2 = Agave.get_reserves_tokens(f1, 'latest')
    print(f2)


    ```

    ```
    output:
    ['0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83', '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', '0xE2e73A1c69ecF83F464EFCE6A5be353a37cA09b2', '0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb', '0x8e5bBbb09Ed1ebdE8674Cda39A0c169401db4252', '0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1', '0x21a42669643f45Bc0e086b8Fc2ed70c23D67509d', '0x4ECaBa5870353805a9F068101A40E0f32ed605C6']
    ```
    </details>

  ### 2: get_reserves_tokens_balances(web3, wallet, block, blockchain, decimals=True)

  > Description: function returns reserved token balances for given wallet address

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Agave

    web3 = get_node(Chain.GNOSIS, 'latest', 0)

    f2 = Agave.get_reserves_tokens_balances(web3, '0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', Chain.GNOSIS)

    print(f2)


    ```

    ```
    output: []
    
    ```
    </details>


  ### 3: get_data(wallet, block, blockchain, execution=1, web3=None, index=1, decimals=True)

  > Description: function returns agave data for given wallet address

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Agave

    f3 = Agave.get_data('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', Chain.GNOSIS)

    print(f3)


    ```

    ```
    output: None
    
    ```
    </details>

  ### 4: get_all_rewards(wallet, block, blockchain, execution=1, web3=None, index=0, decimals=True)

  > Description: function returns all rewards for given wallet on agave protocol

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Agave

    f4 = Agave.get_all_rewards('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', Chain.GNOSIS)

    print(f4)


    ```

    ```
    output: [['0x3a97704a1b25F08aa230ae53B352e2e72ef52843', 0.0]]
    
    ```
    </details>

  ### 5: underlying(wallet, block, blockchain, execution=1, web3=None, index=0, decimals=True, reward=False)

  > Description: function returns underlying tokens for given wallet from agave protocol

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Agave

    f5 = Agave.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', Chain.GNOSIS, reward=True)

    print(f5)


    ```

    ```
    output: [[], [['0x3a97704a1b25F08aa230ae53B352e2e72ef52843', 0.0]]]
    
    ```
    </details>


  </details>

- <details><summary><b>Aura</b></summary>
  
  # Aura

  ## Defined in Aura.py


  ### 1: get_pool_info(booster_contract, lptoken_address, block)

  > Description: function returns pool info for Aura protocol
    ```
    # get_pool_info - Retrieves the result of the pool_info method if there is a match for the lptoken_address - Otherwise it returns None
    # Output: pool_info method return a list with the following data: 
    # [0] lptoken address, [1] token address, [2] gauge address, [3] crvRewards address, [4] stash adress, [5] shutdown bool
    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Aura

    f0 = get_contract('0xA57b8d98dAE62B26Ec3bcC4a365338157060B234', Chain.ETHEREUM)

    f1 = Aura.get_pool_info(f0, '0xCfCA23cA9CA720B6E98E3Eb9B6aa0fFC4a5C08B9', 'latest')

    print(f1)

    ```

    ```
    output: 
    ['0xCfCA23cA9CA720B6E98E3Eb9B6aa0fFC4a5C08B9', '0x70751c02db1a5e48eD333c919A7B94e34a4E07E2', '0x275dF57d2B23d53e20322b4bb71Bf1dCb21D0A00', '0x712CC5BeD99aA06fC4D5FB50Aea3750fA5161D0f', '0xE61df2CE6CC89467bb30f44E0d5cABfCEdc115BE', False]
    
    ```
    </details>


  ### 2: get_rewards(web3, rewarder_contract, wallet, block, blockchain, decimals=True)

  > Description: function returns for given wallet from Aura protocol

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Aura

    web3 = get_node(Chain.ETHEREUM, 'latest', 0)

    f1 = get_contract('0x00A7BA8Ae7bca0B10A32Ea1f8e2a1Da980c6CAd2', Chain.ETHEREUM)

    f2 = Aura.get_rewards(web3, f1, '0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', Chain.ETHEREUM)

    print(f2)

    ```

    ```
    output: ['0xba100000625a3754423978a60c9317c58a424e3D', 4017.2429829677944]
    
    ```
    </details>


  ### 3: get_extra_rewards(web3, rewarder_contract, wallet, block, blockchain, decimals=True)

  > Description: function returns extra rewards from Aura protocol for given wallet


  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Aura

    web3 = get_node(Chain.ETHEREUM, 'latest', 0)

    f1 = get_contract('0x00A7BA8Ae7bca0B10A32Ea1f8e2a1Da980c6CAd2', Chain.ETHEREUM)

    f3 = Aura.get_extra_rewards(web3, f1, '0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', Chain.ETHEREUM)

    print(f3)


    ```

    ```
    output: [['0xA13a9247ea42D743238089903570127DdA72fE44', 30.77849807228373]]
    
    ```
    </details>

  ### 4: get_extra_rewards_airdrop(wallet, block, blockchain, execution=1, web3=None, index=0, decimals=True)

  > Description: function returns extra rewards/airdrop for given wallet by Aura protocol

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Aura

    f4 = Aura.get_extra_rewards_airdrop('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', Chain.ETHEREUM)

    print(f4)

    ```

    ```
    output: []
    
    ```
    </details>

  ### 5: get_aura_mint_amount(web3, bal_earned, block, blockchain, decimals=True)

  ** Help needed **

  > Description: function returns ...

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Aura

    ```

    ```
    output: []
    
    ```
    </details>

  ### 6: get_all_rewards(wallet, lptoken_address, block, blockchain, execution=1, web3=None, index=0, decimals=True, bal_rewards_contract=None)

  > Description: function returns all the rewards for givrn wallet on/by Aura protocol

    ```
    # Output:
    # 1 - List of Tuples: [aura_token_address, locked_balance]
    # 2 - List of Tuples: [reward_token_address, balance]

    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Aura

    f6 = Aura.get_all_rewards('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0xCfCA23cA9CA720B6E98E3Eb9B6aa0fFC4a5C08B9', 'latest', Chain.ETHEREUM)

    print(f6)

    ```

    ```
    output: 
    [['0xba100000625a3754423978a60c9317c58a424e3D', 182.74770874952657], ['0xC0c293ce456fF0ED870ADd98a0828Dd4d2903DBF', 656.3832186003915]]
    
    ```
    </details>

  ### 7: get_locked(wallet, block, blockchain, execution=1, web3=None, index=0, reward=False, decimals=True)

  > Description: function returns locked token on Aura protocol for given wallet address
    ```
    # Output:
    # 1 - List of Tuples: [aurabal_token_address, staked_balance]
    # 2 - List of Tuples: [reward_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Aura

    f7 = Aura.get_locked('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', Chain.ETHEREUM)

    print(f7)

    ```

    ```
    output: 
    [['0xC0c293ce456fF0ED870ADd98a0828Dd4d2903DBF', 1180484.6172952577]]
    
    ```
    </details>


  ### 8: get_staked(wallet, block, blockchain, web3=None, execution=1, index=0, reward=False, decimals=True)

  > Description: function returns staked token for given wallet on Aura protocol

    ```
    # Output:
    # 1 - List of Tuples: [aurabal_token_address, staked_balance]
    # 2 - List of Tuples: [reward_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Aura

    f8 = Aura.get_staked('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', Chain.ETHEREUM)

    print(f8)

    ```

    ```
    output: 
    [['0x616e8BfA43F920657B3497DBf40D6b1A02D4608d', 340828.48444727337]]
    
    ```
    </details>


  ### 9: underlying(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, reward=False, no_balancer_underlying=False, decimals=True)

  > Description: function returns underlying tokens for given wallter from Aura protocol

    ```
    # Output: a list with 2 elements:
    # 1 - List of Tuples: [liquidity_token_address, balance, staked_balance] | [liquidity_token_address, staked_balance] -> depending on 'no_balancer_underlying' value 
    # 2 - List of Tuples: [reward_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Aura

    f9 = Aura.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0xCfCA23cA9CA720B6E98E3Eb9B6aa0fFC4a5C08B9', 'latest', Chain.ETHEREUM)

    print(f9)

    ```

    ```
    output: 
    [['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 95.43873343809126], ['0xC0c293ce456fF0ED870ADd98a0828Dd4d2903DBF', 83620.16903591678]]
    
    ```
    </details>

  ### 10: pool_balances(lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True)

  > Description: function returns pool balances for given lptoken address

    ```
    # Output: a list with 2 elements:
    # 1 - List of Tuples: [liquidity_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Aura

    f10 = Aura.pool_balances('0xCfCA23cA9CA720B6E98E3Eb9B6aa0fFC4a5C08B9', 'latest', Chain.ETHEREUM)

    print(f10)


    ```

    ```
    output: 
    [['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 2680.4587867269847], ['0xC0c293ce456fF0ED870ADd98a0828Dd4d2903DBF', 2348526.7329675243]]
    ```
    </details>


  ### 11: update_db()

  ** Help needed **

  > Description: function updates the db

  </details>

- <details><summary><b>Balancer</b></summary>

  # Balancer

  ## Defined in Balancer.py

  ### 1: get_lptoken_data(lptoken_address, block, blockchain, web3=None, execution=1, index=0)

  > Description: function returns lp token data from balancer protocol

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Balancer

    f1 = Balancer.get_lptoken_data('0x7B50775383d3D6f0215A8F290f2C9e2eEBBEceb2', 'latest', Chain.ETHEREUM)

    print(f1)


    ```

    ```
    output: 
    {'contract': <web3._utils.datatypes.Contract object at 0x7f3c66cb6500>, 'poolId': b'{PwS\x83\xd3\xd6\xf0!Z\x8f)\x0f,\x9e.\xeb\xbe\xce\xb2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfe', 'decimals': 18, 'totalSupply': 4025945672168376636231543, 'isBoosted': True, 'bptIndex': 1}
    ```
    </details>


  ### 2: get_bal_rewards(web3, gauge_contract, wallet, block, blockchain, decimals=True)

  > Description: function returns total balancer rewards for given wallet
  and to a specific Gauge

    ```
    # Output:
    # 1 - Tuples: [bal_token_address, balance]
    ```

  ** Help needed **

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Balancer

    
    web3 = get_node(Chain.ETHEREUM, 'latest', 0)
    f1 = get_contract('0x68d019f64A7aa97e2D4e7363AEE42251D08124Fb', Chain.ETHEREUM)

    f2 = Balancer.get_bal_rewards(web3, 'f1', '0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', Chain.ETHEREUM)

    print(f2)


    ```

    ```
    output: 
    

    ```
    </details>


  ### 3: get_rewards(web3, gauge_contract, wallet, block, blockchain, decimals=True)

  > Description: function returns rewards for the given wallet by balancer protocol

    ```
    # Output:
    # 1 - List of Tuples: [reward_token_address, balance]
    
    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Balancer

    web3 = get_node(Chain.ETHEREUM, 'latest', 0)
    f1 = get_contract('0x68d019f64A7aa97e2D4e7363AEE42251D08124Fb', Chain.ETHEREUM)
    f3 = Balancer.get_rewards(web3, f1, '0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', Chain.ETHEREUM, decimals=True)
    print(f3)

    ```

    ```
    output: []
    
    ```
    </details>


  ### 4: get_vebal_rewards(web3, wallet, block, blockchain, decimals=True)

  > Description: function returns vebal rewards for given wallet by Balancer protocol

    ```
    # Output:
    # 1 - List of Tuples: [reward_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Balancer

    web3 = get_node(Chain.ETHEREUM, 'latest', 0)
    f4 = Balancer.get_vebal_rewards(web3, '0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', Chain.ETHEREUM, decimals=True)
    print(f4)

    ```

    ```
    output: 
    [['0xba100000625a3754423978a60c9317c58a424e3D', 17.470227018260175], ['0x7B50775383d3D6f0215A8F290f2C9e2eEBBEceb2', 111.44084143506045], ['0xA13a9247ea42D743238089903570127DdA72fE44', 25.141921181623832]]
    
    ```
    </details>


  ### 5: get_all_rewards(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True, gauge_address=None)

  > Description: function returns all the rewards for the given wallet by Balancer protocol

    ```
    # Output:
    # 1 - List of Tuples: [reward_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Balancer
    
    f5 = Balancer.get_all_rewards('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0x7B50775383d3D6f0215A8F290f2C9e2eEBBEceb2', 'latest', Chain.ETHEREUM)
    
    print(f5)


    ```

    ```
    output: [['0xba100000625a3754423978a60c9317c58a424e3D', 0.0]]
    
    ```
    </details>


  ### 6: underlying(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, reward=False, aura_staked=None, decimals=True)

  > Description: function returns underlying token for given wallet on Balancer protocol

    ```
    # Output: a list with 2 elements:
    # 1 - List of Tuples: [liquidity_token_address, balance, staked_balance, locked_balance]
    # 2 - List of Tuples: [reward_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Balancer
    
    f6 = Balancer.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0x7B50775383d3D6f0215A8F290f2C9e2eEBBEceb2', 'latest', Chain.ETHEREUM)
    
    print(f6)


    ```

    ```
    output: 

    [['0xdAC17F958D2ee523a2206206994597C13D831ec7', 1.847331235617916e-12, 0.0, 0.0], ['0x6B175474E89094C44Da98b954EedeAC495271d0F', 1.8079866128717203e-12, 0.0, 0.0], ['0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 1.7579658914113204e-12, 0.0, 0.0]]
    
    ```
    </details>


  ### 7: pool_balances(lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True)

  > Description: function returns pool balances on Balancer protocol

    ```
    # Output: a list with 1 element:
    # 1 - List of Tuples: [liquidity_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Balancer
    
    f7 = Balancer.pool_balances('0x7B50775383d3D6f0215A8F290f2C9e2eEBBEceb2', 'latest', Chain.ETHEREUM) 

    print(f7)

    ```

    ```
    output: 

    [['0xdAC17F958D2ee523a2206206994597C13D831ec7', 1396069.6262515152], ['0x6B175474E89094C44Da98b954EedeAC495271d0F', 1366336.012581301], ['0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 1328534.2340286463]]

    ```
    </details>


  ### 8: swap_fees(lptoken_address, block_start, block_end, blockchain, web3=None, execution=1, index=0, decimals=True)

  > Description: function returns the swap fees for given lptoken on Balancer protocol

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Balancer
    
    f8 = Balancer.swap_fees('0x7B50775383d3D6f0215A8F290f2C9e2eEBBEceb2', 16374265, 'latest', Chain.ETHEREUM)

    print(f8)

    ```

    ```
    output: 
    {'swaps': [{'block': 16376941, 'tokenIn': '0x9210F1204b5a24742Eba12f710636D76240dF3d0', 'amountIn': 0.8095032036253991}, {'block': 16378850, 'tokenIn': '0x804CdB9116a10bB78768D3252355a1b18067bF8f', 'amountIn': 0.9885184780730925}]}
    
    ```
    </details>


  </details>

- <details><summary><b>Bancor</b></summary>

  # Bancor

  ## Defined in Bancor.py

  ### 1: underlying(token_address, wallet, block, blockchain, web3=None, execution=1, index=0, decimals=True, reward=False)

  > Description: function returns the underlying token from bancor protocol for given wallet

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Bancor

    f1 = Bancor.underlying('0x36FAbE4cAeF8c190550b6f93c306A5644E7dCef6', '0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', Chain.ETHEREUM)

    print(f1)

    ```

    ```
    output: 
    [['0x803bEF1736CDdf2A537176cf3C64579C3867A881', 41633.599736141], ['0x1F573D6Fb3F13d689FF844B4cE37794d79a7FF1C', 0.0]]
    ```
    </details>


  ### 2: underlying_all(wallet, block, blockchain, web3=None, execution=1, index=0, decimals=True, reward=False)

  > Description: function returns all underlying tokens for given wallet

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Bancor

    f2 = Bancor.underlying_all('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', Chain.ETHEREUM)

    print(f2)
    ```

    ```
    output: None
    ```
    </details>

  </details>

- <details><summary><b>Convex</b></summary>

  # Convex

  ## Defined in Convex.py

  ### 1: get_pool_info(lptoken_address, block)

  > Description: function returns pool related info for given lp token

    ```
    # Output: pool_info method return a list with the following data: 
    # [0] lptoken address, [1] token address, [2] gauge address, [3] crvRewards address, [4] stash adress, [5] shutdown bool
    ```

  - <details><summary><b>Example</b></summary>

    ```

    from defyes import *

    from defyes.functions import *

    from defyes import Convex

    f1 = Convex.get_pool_info('0x9fC689CCaDa600B6DF723D9E47D84d76664a1F23', 'latest')

    print(f1)

    ```

    ```
    output:
    ['0x9fC689CCaDa600B6DF723D9E47D84d76664a1F23', '0xA1c3492b71938E144ad8bE4c2fB6810b01A43dD8', '0xBC89cd85491d81C6AD2954E6d0362Ee29fCa8F53', '0x8B55351ea358e5Eda371575B031ee24F462d503e', '0x0000000000000000000000000000000000000000', False]

    ```
    </details>


  ### 2: get_rewards(web3, rewarder_contract, wallet, block, blockchain, decimals=True)

  > Description: function returns rewards for given wallet on Conexx protocol

    ```
    # Output:
    # 1 - Tuples: [token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```

    from defyes import *

    from defyes.functions import *

    from defyes import Convex

    web3 = get_node(Chain.ETHEREUM, 'latest', 0)
    f1 = get_contract('0xf34DFF761145FF0B05e917811d488B441F33a968', Chain.ETHEREUM)
    f2 = Convex.get_rewards(web3, f1, '0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', Chain.ETHEREUM)
    print(f2)

    ```

    ```
    output:
    ['0xD533a949740bb3306d119CC777fa900bA034cd52', 1376.4851165071896]

    ```
    </details>

  ### 3: get_extra_rewards(web3, crv_rewards_contract, wallet, block, blockchain, decimals=True)

  > Description: function returns extra rewards by convex protocol for given wallet

    ```
    # 1 - List of Tuples: [reward_token_address, balance]
    ```
  - <details><summary><b>Example</b></summary>

    ```

    from defyes import *

    from defyes.functions import *

    from defyes import Convex

    web3 = get_node(Chain.ETHEREUM, 'latest', 0)
    f1 = get_contract('0xf34DFF761145FF0B05e917811d488B441F33a968', Chain.ETHEREUM)
    f3 = Convex.get_extra_rewards(web3, f1, '0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', Chain.ETHEREUM)
    print(f3)

    ```

    ```
    output: []

    ```
    </details>

  ### 3: get_cvx_mint_amount(web3, crv_earned, block, blockchain, decimals=True)

  ** Help needed **

  > Description: function returns 

  - <details><summary><b>Example</b></summary>

    ```

    from defyes import *

    from defyes.functions import *

    from defyes import Convex

    ```

    ```
    output: []

    ```
    </details>

  ### 4: get_all_rewards(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True, crv_rewards_contract=None)

  > Description: function returns all rewards for given wallet on Convex protocol

    ```
    # Output:
    # 1 - List of Tuples: [reward_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```

    from defyes import *

    from defyes.functions import *

    from defyes import Convex

    f1 = get_contract('0xf34DFF761145FF0B05e917811d488B441F33a968', Chain.ETHEREUM)
    f4 = Convex.get_all_rewards('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'f1', 'latest', Chain.ETHEREUM)
    print(f4)

    ```

    ```
    output: None

    ```
    </details>


  ### 5: get_locked(wallet, block, blockchain, web3=None, execution=1, index=0, reward=False, decimals=True)

  > Description: function returns locked tokens for given wallet on Convex protocol

    ```
    # Output:
    # 1 - List of Tuples: [cvx_token_address, locked_balance]
    # 2 - List of Tuples: [reward_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```

    from defyes import *

    from defyes.functions import *

    from defyes import Convex

    f5 = Convex.get_locked('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', Chain.ETHEREUM)
    
    print(f5)

    
    ```

    ```
    output:
    [['0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B', 8943.594875319563]]

    ```
    </details>

  ### 6: get_staked(wallet, block, blockchain, web3=None, execution=1, index=0, reward=False, decimals=True)

  > Description: function returns staked token for given wallet on Convex protocol

    ```
    # Output:
    # 1 - List of Tuples: [cvx_token_address, staked_balance]
    # 2 - List of Tuples: [reward_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```

    from defyes import *

    from defyes.functions import *

    from defyes import Convex

    f6 = Convex.get_staked('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', Chain.ETHEREUM)
    
    print(f6)
    
    ```

    ```
    output:
    [['0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B', 0.0]]

    ```
    </details>

  ### 7: underlying(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, reward=False, decimals=True, no_curve_underlying=False)

  > Description: function returns underlying token for given wallet on Convex protocol

    ```
    # Output: a list with 2 elements:
    # 1 - List of Tuples: [liquidity_token_address, balance, staked_balance] | [liquidity_token_address, staked_balance] -> depending on 'no_curve_underlying' value 
    # 2 - List of Tuples: [reward_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```

    from defyes import *

    from defyes.functions import *

    from defyes import Convex

    f7 = Convex.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0x9fC689CCaDa600B6DF723D9E47D84d76664a1F23', 'latest', Chain.ETHEREUM)
    
    print(f7)
    
    ```

    ```
    output:
    [['0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643', 0.0], ['0x39AA39c021dfbaE8faC545936693aC917d5E7563', 0.0], ['0xdAC17F958D2ee523a2206206994597C13D831ec7', 0.0]]

    ```
    </details>

  ### 8: pool_balances(lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True)

  > Description: function returns pool balance for given lp token on Convex protocol

    ```
    # Output: a list with 2 elements:
    # 1 - List of Tuples: [liquidity_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```

    from defyes import *

    from defyes.functions import *

    from defyes import Convex

    f8 = Convex.pool_balances('0x9fC689CCaDa600B6DF723D9E47D84d76664a1F23', 'latest', Chain.ETHEREUM)
    
    print(f8)
    
    ```

    ```
    output:
    
    [['0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643', 5627718.31410783], ['0x39AA39c021dfbaE8faC545936693aC917d5E7563', 5115086.87914827], ['0xdAC17F958D2ee523a2206206994597C13D831ec7', 117437.410424]]
    ```
    </details>

  ### 9: update_db()

  > Description: function updates the Convex db

  *** Help Needed ***


  </details>

- <details><summary><b>Curve</b></summary>

  # Curve

  ## Defined in Curve.py

  ### 1: get_registry_contract(web3, id, block, blockchain)

  > Dexcription: function returns registry contract object using given id and blockchain

    ``` 
    # id = 0 -> Registry for Regular Pools
    # id = 3 -> Registry for Factory Pools
    # id = 5 -> Registry for Crypto V2 Pools
    # id = 6 -> Registry for Crypto Factory Pools

    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Curve

    web3 = get_node(Chain.ETHEREUM, 'latest', 0)
    f1 = Curve.get_registry_contract(web3, 3, 'latest', Chain.ETHEREUM)
    print(f1)

    ```

    ```
    output: <web3._utils.datatypes.Contract object at 0x7fece881a980>

    ```
    </details>

  ### 2: get_pool_gauge_address(web3, pool_address, lptoken_address, block, blockchain)

  > Description: function returns pool gauge address on Curve protocol

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Curve

    web3 = get_node(Chain.GNOSIS, 'latest', 0)
    
    web3 = get_node(Chain.GNOSIS, 'latest', 0)
    
    f2 = Curve.get_pool_gauge_address(web3, '0x7f90122BF0700F9E7e1F688fe926940E8839F353', '0x1337BedC9D22ecbe766dF105c9623922A27963EC', 'latest', Chain.GNOSIS)

    print(f2)

    ```

    ```
    output: 0xB721Cc32160Ab0da2614CC6aB16eD822Aeebc101

    ```
    </details>


  ### 3: get_gauge_version(gauge_address, block, blockchain, web3=None, execution=1, index=0, only_version=True)

  > Description: function returns gauge version for given gauge on Curve protocol

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Curve

    f3 = Curve.get_gauge_version('0x1891E46859DBf78EeEfb652425755494eE8aD7bf', 'latest', Chain.GNOSIS)

    print(f3)

    ```

    ```
    output: ChildGauge

    ```
    </details>


  ### 4: get_pool_address(web3, lptoken_address, block, blockchain)

  > Description: function returns pool address for given lptoken on Curve protocol

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Curve

    web3 = get_node(Chain.GNOSIS, 'latest', 0)
    
    f4 = Curve.get_pool_address(web3, '0x1337BedC9D22ecbe766dF105c9623922A27963EC', 'latest', Chain.GNOSIS)
    
    print(f4)


    ```

    ```
    output: 0x7f90122BF0700F9E7e1F688fe926940E8839F353

    ```
    </details>


  ### 5: get_pool_data(web3, minter, block, blockchain):

  > Description: function returns pool data for Curver protocol


  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Curve

    web3 = get_node(Chain.ETHEREUM, 'latest', 0)
    
    f5 = Curve.get_pool_data(web3, '0xD51a44d3FaE010294C616388b506AcdA1bfAAE46', 'latest', Chain.ETHEREUM)

    print(f5)


    ```

    ```
    output: 

    {'contract': <web3._utils.datatypes.Contract object at 0x7f283c7f67d0>, 'is_metapool': False, 'coins': {0: '0xdAC17F958D2ee523a2206206994597C13D831ec7', 1: '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599', 2: '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'}}

    ```
    </details>

  ### 6: get_lptoken_data(lptoken_address, block, blockchain, web3=None, execution=1, index=0)

  > Description: function returns lp token data

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Curve

    f6 = Curve.get_lptoken_data('0xc4AD29ba4B3c580e6D59105FFf484999997675Ff', 'latest', Chain.ETHEREUM)

    print(f6)

    ```

    ```
    output: 
    {'contract': <web3._utils.datatypes.Contract object at 0x7f5b1cbea770>, 'minter': '0xD51a44d3FaE010294C616388b506AcdA1bfAAE46', 'decimals': 18, 'totalSupply': 182450506161827209744987}  

    ```
    </details>


  ### 7: get_all_rewards(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True, gauge_address=None)

  > Description: function returns all the rewards for the given wallet and lp token on Curve protocol

    ```
    # Output:
    # 1 - List of Tuples: [reward_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Curve

    f7 = Curve.get_all_rewards('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0xc4AD29ba4B3c580e6D59105FFf484999997675Ff', 'latest', Chain.ETHEREUM)

    print(f7)

    ```

    ```
    output: [['0xD533a949740bb3306d119CC777fa900bA034cd52', 0.0]]
    
    ```
    </details>


  ### 8: underlying(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, reward=False, decimals=True, convex_staked=None, gauge_address=None)

  > Description: function returns underlying tokens for given wallet with given lptoken on Curve protocol

    ```
    # Output: a list with 2 elements:
    # 1 - List of Tuples: [liquidity_token_address, balance, staked_balance]
    # 2 - List of Tuples: [reward_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Curve

    f8 = Curve.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0x1337BedC9D22ecbe766dF105c9623922A27963EC', 'latest', Chain.GNOSIS )

    print(f8)

    ```

    ```
    output: 
    [['0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 0.0, 0.0], ['0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83', 0.0, 0.0], ['0x4ECaBa5870353805a9F068101A40E0f32ed605C6', 0.0, 0.0]]
    
    ```
    </details>


  ### 9: underlying_amount(lptoken_amount, lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True)

  > Description: 

  ** Help Needed **


  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Curve

    
    ```

    ```
    output: 
    
    ```
    </details>

  ### 10: pool_balances(lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True, meta=False)

  > Description: function returns pool balances of given lptoken on Curve protocol

    ```
    # Output: a list with 1 elements:
    # 1 - List of Tuples: [liquidity_token_address, balance]
    ```
  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Curve

    f10 = Curve.pool_balances('0x1337BedC9D22ecbe766dF105c9623922A27963EC', 'latest', Chain.GNOSIS)

    print(f10)

    
    ```

    ```
    output: 
    [['0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 3097529.0538003724], ['0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83', 3073195.827396], ['0x4ECaBa5870353805a9F068101A40E0f32ed605C6', 3086394.257995]]
    
    ```
    </details>


  ### 11: swap_fees(lptoken_address, block_start, block_end, blockchain, web3=None, execution=1, index=0, decimals=True)

  > Description: function returns swap fees for given lp token for given range on Curve protocol

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Curve

    f11 = Curve.swap_fees('0x1337BedC9D22ecbe766dF105c9623922A27963EC', 25913602, 'latest', Chain.GNOSIS)

    print(f11)

    
    ```

    ```
    output: 
    {'swaps': [{'block': 25913682, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.0019992133127874276}, {'block': 25913701, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.007333559800511542}, {'block': 25913721, 'tokenOut': '0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83', 'amountOut': 0.6397394164}, {'block': 25913783, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.0008607565751133651}, {'block': 25913910, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.037022720405197725}, {'block': 25913948, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.039984303471116825}, {'block': 25913970, 'tokenOut': '0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83', 'amountOut': 0.4002363776}, {'block': 25914114, 'tokenOut': '0x4ECaBa5870353805a9F068101A40E0f32ed605C6', 'amountOut': 0.007996171600000001}, {'block': 25914144, 'tokenOut': '0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83', 'amountOut': 0.0066172976}, {'block': 25914200, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.0014729267096921916}, {'block': 25914330, 'tokenOut': '0x4ECaBa5870353805a9F068101A40E0f32ed605C6', 'amountOut': 0.0039983932}, {'block': 25914416, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.008602286827199044}, {'block': 25914750, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.022511488698351036}, {'block': 25914759, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.006614704715056072}, {'block': 25914759, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.6997249291194675}, {'block': 25915143, 'tokenOut': '0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83', 'amountOut': 0.13503600880000002}, {'block': 25915224, 'tokenOut': '0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83', 'amountOut': 0.11770507120000001}, {'block': 25915235, 'tokenOut': '0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83', 'amountOut': 0.117932982}, {'block': 25915309, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.021514701714473644}, {'block': 25915340, 'tokenOut': '0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83', 'amountOut': 0.005720752000000001}, {'block': 25915455, 'tokenOut': '0x4ECaBa5870353805a9F068101A40E0f32ed605C6', 'amountOut': 1.499395634}, {'block': 25915655, 'tokenOut': '0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83', 'amountOut': 0.05997549320000001}, {'block': 25915684, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.00030144913310451685}, {'block': 25915782, 'tokenOut': '0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83', 'amountOut': 0.0219822164}, {'block': 25915803, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.02242247669985942}, {'block': 25915834, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.0004494915495654226}, {'block': 25915864, 'tokenOut': '0x4ECaBa5870353805a9F068101A40E0f32ed605C6', 'amountOut': 0.0843659144}, {'block': 25915973, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.02079185759339624}, {'block': 25916016, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.09113021136366664}, {'block': 25916018, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.001970104549943838}, {'block': 25916024, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.0011432944757581813}, {'block': 25916028, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.0014962398019174262}, {'block': 25916156, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.2998824374160615}, {'block': 25916435, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.0006173702201516521}]}
    
    ```
  </details>


  </details>

- <details><summary><b>Elk</b></summary>

  # Elk

  ## Defined in Elk.py

  ### 1: get_lptoken_data(lptoken_address, block, blockchain, web3=None, execution=1, index=0)

  > Description: function returns lp token data on ELK protocol

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Elk


    f1 = Elk.get_lptoken_data('0xA27E5775317F3f301B5b08BabCdE0a20FEAE7f09', 'latest', Chain.ETHEREUM)

    print(f1)

    ```

    ```
    output:
    {'contract': <web3._utils.datatypes.Contract object at 0x7fb03eef26b0>, 'decimals': 18, 'totalSupply': 3079557346471436960125, 'token0': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'token1': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'reserves': [29056721408238148310, 347561671694311785474636, 1673509307], 'kLast': 0, 'virtualTotalSupply': 3079557346471436960125}
    
    ```
    </details>


  ### 2: get_pool_address(web3, token0, token1, block, blockchain)

  > Description: function returns pool address based on given token pair on Elk protocol


  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Elk

    web3 = get_node(Chain.ETHEREUM, 'latest', 0)
    
    f2 = Elk.get_pool_address(web3, '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'latest', Chain.ETHEREUM)
    
    print(f2)
    
    ```

    ```
    output:
    0xF220eA963D27Ebe782f09403017B29692A4fC4aE
    
    ```
    </details>


  ### 3: get_elk_rewards(web3, pool_contract, wallet, block, blockchain, decimals=True)

  > Description: function returns elk rewards for given pool address for given wallet

    ```
    # Output:
    # 1 - Tuple: [elk_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Elk

    web3 = get_node(Chain.ETHEREUM, 'latest', 0)
    f2 = get_contract('0xF220eA963D27Ebe782f09403017B29692A4fC4aE', Chain.ETHEREUM)
    f3 = Elk.get_elk_rewards(web3, f2, '0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', Chain.ETHEREUM)

    print(f3)

    ```

    ```
    output: ['0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 0.0]
    
    
    ```
    </details>

  ### 4: get_booster_rewards(web3, pool_contract, wallet, block, blockchain, decimals=True)

  > Description: function returns booster rewards on given pool address for given wallet

    ```
    # Output:
    # 1 - List of Tuples: [reward_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Elk

    web3 = get_node(Chain.ETHEREUM, 'latest', 0)
    f3 = get_contract('0xF220eA963D27Ebe782f09403017B29692A4fC4aE', Chain.ETHEREUM)
    f4 = Elk.get_booster_rewards(web3, f3, '0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', Chain.ETHEREUM)
    
    print(f4)

    ```

    ```
    output: None
    
    ```
    </details>


  ### 5: get_all_rewards(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True, pool_contract=None)

  > Description: function returns all rewards for given wallet for given lp token

    ```
    # Output:
    # 1 - List of Tuples: [reward_token_address, balance]
    ```
  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Elk

    f5 = Elk.get_all_rewards('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0xF220eA963D27Ebe782f09403017B29692A4fC4aE', 'latest', Chain.ETHEREUM)

    print(f5)

    ```

    ```
    output: None
    
    ```
    </details>


  ### 6: underlying(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True, reward=False)

  > Description: function returns underlying tokens for given wallet for given lp token on Elk protocol

    ```
    # Output: a list with 2 elements:
    # 1 - List of Tuples: [liquidity_token_address, balance, staked_balance]
    # 2 - List of Tuples: [reward_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Elk

    f6 = Elk.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0xA27E5775317F3f301B5b08BabCdE0a20FEAE7f09', 'latest', Chain.ETHEREUM)

    print(f6)

    ```

    ```
    output: 

    [['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 0.0, 0.0], ['0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 0.0, 0.0]]
    
    ```
    </details>


  ### 7: pool_balances(lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True)

  > Description: function retirns pool balances for given lp token

    ``` 
    # 1 - List of Tuples: [liquidity_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Elk

    f7 = Elk.pool_balances('0xA27E5775317F3f301B5b08BabCdE0a20FEAE7f09', 'latest', Chain.ETHEREUM)
    
    print(f7)

    ```

    ```
    output: 
    
    [['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 29.056721408238147], ['0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 347561.6716943118]]
    
    ```
    </details>


  ### 8: swap_fees(lptoken_address, block_start, block_end, blockchain, web3=None, execution=1, index=0, decimals=True)

  > Description: function returns swap fees for given lp token

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Elk

    f8 = Elk.swap_fees('0xA27E5775317F3f301B5b08BabCdE0a20FEAE7f09', 16380015, 'latest', Chain.ETHEREUM)

    print(f8)

    ```

    ```
    output: 
    {'swaps': [{'block': 16381797, 'token': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'amount': 2.889438460326057}, {'block': 16382996, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 3e-09}, {'block': 16385571, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 0.00255}, {'block': 16385667, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 0.0009}, {'block': 16385691, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 9e-06}, {'block': 16385812, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 0.00015}, {'block': 16385831, 'token': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'amount': 26.723058285543605}, {'block': 16385839, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 0.00017571833246287513}, {'block': 16385938, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 6e-05}, {'block': 16385957, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 3.6e-05}, {'block': 16385975, 'token': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'amount': 12.83912818935761}, {'block': 16386009, 'token': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'amount': 0.39853215112316875}, {'block': 16386450, 'token': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'amount': 31.327314122523138}, {'block': 16386451, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 0.0014496276567174053}, {'block': 16386524, 'token': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'amount': 36.478903268343565}, {'block': 16386527, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 0.0018}, {'block': 16386537, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 0.0005028085391423697}, {'block': 16386559, 'token': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'amount': 23.07109673165644}, {'block': 16386561, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 0.0015010243909154}, {'block': 16387375, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 1.2028675361808711e-05}, {'block': 16387414, 'token': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'amount': 2.957184093901322}, {'block': 16388603, 'token': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'amount': 7.1615954570745695}, {'block': 16388771, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 1.5e-05}, {'block': 16388955, 'token': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'amount': 6.3083888292692265}, {'block': 16388990, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 0.0007353592629198234}, {'block': 16389072, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 0.00021921}, {'block': 16389072, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 0.00255}, {'block': 16389072, 'token': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'amount': 2.65335036}, {'block': 16389108, 'token': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'amount': 9.0}, {'block': 16389299, 'token': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'amount': 11.890786090090941}]}
    
    ```
    </details>

  </details>

- <details><summary><b>Honeyswap</b></summary>

  # Honeyswap

  ## Defined in Honeyswap.py

  ### 1: get_lptoken_data(lptoken_address, block, blockchain, web3=None, execution=1, index=0)

  > Description: function returns lp token data on Honeyswap protoocl


  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Honeyswap

    f1 = Honeyswap.get_lptoken_data('0xCd9652F006EFDE64f07030F10A1945EAD8AC1855', 'latest', Chain.ETHEREUM)
    
    print(f1)

    ```

    ```
    output:
    {'contract': <web3._utils.datatypes.Contract object at 0x7fba31e8a710>, 'decimals': 18, 'totalSupply': 108503144715306467026, 'token0': '0x1957d368f6038F09faaE020d485b35718E0Eed1A', 'token1': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'reserves': [763270497078084747756, 15742597871023746342, 1607901903], 'kLast': 0, 'virtualTotalSupply': 1.3020377365836775e+20}  
    
    ```
    </details>


  ### 2: underlying(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True)

  > Description: function returns underlying tokens for given wallet with given lptoken

    ```
    # Output: a list with 1 element:
    # 1 - List of Tuples: [liquidity_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Honeyswap

    f2 = Honeyswap.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0xCd9652F006EFDE64f07030F10A1945EAD8AC1855', 'latest', Chain.ETHEREUM)

    print(f2)

    ```

    ```
    output:
    [['0x1957d368f6038F09faaE020d485b35718E0Eed1A', 0.0], ['0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 0.0]]

    ```
    </details>


  ### 3: pool_balances(lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True)

  > Description: function returns pool balances for given lp token on Honeyswap protocol

    ```
    # Output: a list with 1 element:
    # 1 - List of Tuples: [liquidity_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Honeyswap

    f3 = Honeyswap.pool_balances('0xCd9652F006EFDE64f07030F10A1945EAD8AC1855', 'latest', Chain.ETHEREUM)

    print(f3)
    
    ```

    ```
    output:
    [['0x1957d368f6038F09faaE020d485b35718E0Eed1A', 763.2704970780848], ['0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 15.742597871023746]]

    ```
    </details>

  ### 4: swap_fees(lptoken_address, block_start, block_end, blockchain, web3=None, execution=1, index=0, decimals=True)

  > Description: function returns swap fees for given lp token for give reange of blocks

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Honeyswap

    f4 = Honeyswap.swap_fees('0xCd9652F006EFDE64f07030F10A1945EAD8AC1855', 0, 'latest', Chain.ETHEREUM)

    print(f4)

    ```

    ```
    output:
    {'swaps': [{'block': 11134367, 'token': '0x1957d368f6038F09faaE020d485b35718E0Eed1A', 'amount': 0.0005262109004007418}, {'block': 11134380, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.0038122294599445485}, {'block': 11134649, 'token': '0x1957d368f6038F09faaE020d485b35718E0Eed1A', 'amount': 0.000497428365687157}, {'block': 11134961, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.004008351883662104}, {'block': 11134984, 'token': '0x1957d368f6038F09faaE020d485b35718E0Eed1A', 'amount': 0.025735010568652947}, {'block': 11135972, 'token': '0x1957d368f6038F09faaE020d485b35718E0Eed1A', 'amount': 0.23927241967672228}, {'block': 11135972, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.001371294269959149}, {'block': 11136386, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.00149518324360386}, {'block': 11138426, 'token': '0x1957d368f6038F09faaE020d485b35718E0Eed1A', 'amount': 1.5}, {'block': 11138426, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.0005880163841135043}, {'block': 11141757, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.003}, {'block': 11143948, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.0009482496689891964}, {'block': 11153516, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.0009999}, {'block': 11153523, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.0015}, {'block': 11153530, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.0005001}, {'block': 11153581, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.0018}, {'block': 11168389, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.0020655702056233145}, {'block': 11210669, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.005054900815379415}, {'block': 11211315, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.005111990858317916}, {'block': 11211817, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.005679169733007941}, {'block': 11212191, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.0165}, {'block': 11212438, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.018518323978912336}, {'block': 11213214, 'token': '0x1957d368f6038F09faaE020d485b35718E0Eed1A', 'amount': 0.16961917796935855}, {'block': 11213827, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.023760662104344098}, {'block': 11216926, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.008840951952023836}, {'block': 11216935, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.010587407899320654}, {'block': 11216941, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.012907693813954431}, {'block': 11216952, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.016084013197213927}, {'block': 11216959, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.02059631880854048}, {'block': 11216965, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.02731565993218982}, {'block': 11216969, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.033512834207083994}, {'block': 11216969, 'token': '0x1957d368f6038F09faaE020d485b35718E0Eed1A', 'amount': 0.04565053353647096}, {'block': 11216973, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.03537631473540627}, {'block': 11218589, 'token': '0x1957d368f6038F09faaE020d485b35718E0Eed1A', 'amount': 0.02682485834232684}, {'block': 11229905, 'token': '0x1957d368f6038F09faaE020d485b35718E0Eed1A', 'amount': 0.05504515223226972}, {'block': 11240721, 'token': '0x1957d368f6038F09faaE020d485b35718E0Eed1A', 'amount': 0.16473663231733446}, {'block': 11243062, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.024}, {'block': 11246252, 'token': '0x1957d368f6038F09faaE020d485b35718E0Eed1A', 'amount': 0.3}, {'block': 11247278, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.015323293667631526}, {'block': 11428790, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.0011079232513274775}, {'block': 11447567, 'token': '0x1957d368f6038F09faaE020d485b35718E0Eed1A', 'amount': 1.5}]}
    

    ```
    </details>

  </details>

- <details><summary><b>Maker</b></summary>

  # Maker

  ## Defined in Maker.py

  ### 1: get_vault_data(vault_id, block, web3=None, execution=1, index=0)

  > Description: function returns valut data for given valut id

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Maker

    f1 = Maker.get_vault_data(1, 'latest')
    
    print(f1)

    ```

    ```
    output:
    {'mat': 1.45, 'gem': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'dai': '0x6B175474E89094C44Da98b954EedeAC495271d0F', 'ink': 0.0, 'art': 0.0, 'Art': 193027523.3855285, 'rate': 1.0835304604763405, 'spot': 963.8172413793103, 'line': 368907736.31731033, 'dust': 15000.0}
    
    ```
    </details>


  ### 2: underlying(vault_id, block, web3=None, execution=1, index=0)

  > Description: function returns underlying tokens for given wallet for given vault id on maker protocol

    ```
    # Output:
    # 1 - Tuple: [[collateral_address, collateral_amount], [debt_address, -debt_amount]]
    ```
  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Maker

    f2 = Maker.underlying(1, 'latest')
    
    print(f2)

    ```

    ```
    output:
    [['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 0.0], ['0x6B175474E89094C44Da98b954EedeAC495271d0F', -0.0]]
    
    
    ```
    </details>

  </details>


- <details><summary><b>Qidao</b></summary>

  # QiDao

  ## Defined in QiDao.py

  ### 1: get_vault_address(collateral_address, blockchain)

  > Description: function returns vault address based on given collateral address

  - <details><summary><b>Example</b></summary>

    ```
    
    from defyes import *

    from defyes.functions import *

    from defyes import QiDao

    f1 = QiDao.get_vault_address('0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb', Chain.GNOSIS)

    print(f1)

    ```

    ```
    output: 0x014A177E9642d1b4E970418f894985dC1b85657f
    
    ```
    </details>

  ### 2: get_vault_data(vault_id, collateral_address, block, blockchain, web3=None, execution=1, index=0, decimals=True)

  > Description: function returns vault data based on given vault id and collateral address


  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import QiDao

    f2 = QiDao.get_vault_data(1, '0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb', 'latest', Chain.GNOSIS)

    print(f2)


    ```

    ```
    output: 
    {'collateral_address': '0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb', 'collateral_amount': 0.0, 'collateral_token_usd_value': 96.15, 'debt_address': '0x3F56e0c36d275367b8C502090EDF38289b3dEa0d', 'debt_amount': 0.0, 'debt_token_usd_value': 0.9920834072195736, 'debt_usd_value': 0, 'collateral_ratio': None, 'available_debt_amount': 203205.79297252028, 'liquidation_ratio': 130, 'liquidation_price': None}
    
    ```
    </details>

  ### 3: underlying(vault_id, collateral_address, block, blockchain, web3=None, execution=1, index=0, decimals=True)

  > Description: function returns underlying tokens for given vault id and collateral address

    ```
    # Output:
    # 1 - Tuple: [[collateral_address, collateral_amount], [debt_address, -debt_amount]]
    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import QiDao

    f3 = QiDao.underlying(1, '0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb', 'latest', Chain.GNOSIS)

    print(f3)

    ```

    ```
    output: 
    [['0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb', 0.0], ['0x3F56e0c36d275367b8C502090EDF38289b3dEa0d', 0.0]]
    
    ```
    </details>

  </details>

- <details><summary><b>Reflexer</b></summary>

  # Reflexer

  ## Defined in Reflexer.py

  ### 1: lptoken_underlying(lptoken_address, amount, block, blockchain)

  > Description: function returns underlying tokens for given lp token on Reflexer protocol

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Reflexer

    f1 = Reflexer.lptoken_underlying('0xd6F3768E62Ef92a9798E5A8cEdD2b78907cEceF9', 10000, 'latest', Chain.ETHEREUM)

    print(f1)


    ```

    ```
    output:
    [['0x6243d8cea23066d098a15582d81a598b4e8391f4', 51479.35989733311], ['0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 524.5602730745637]]
    [['0x6243d8cea23066d098a15582d81a598b4e8391f4', 51479.35989733311], ['0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 524.5602730745637]]
    [['0x6243d8cea23066d098a15582d81a598b4e8391f4', 115095.22732025111], ['0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 1172.7881619564894]]
    ```
    </details>


  ### 2: pool_balance(lptoken_address, block, blockchain)

  > Description: function returns pool balance for given lp token

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Reflexer

    f2 = Reflexer.pool_balance('0xd6F3768E62Ef92a9798E5A8cEdD2b78907cEceF9', 'latest', Chain.ETHEREUM)

    print(f2)

    ```

    ```
    output:
    [['0x6243d8cea23066d098a15582d81a598b4e8391f4', 51479.35989733311], ['0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 524.5602730745637]]
    [['0x6243d8cea23066d098a15582d81a598b4e8391f4', 51479.35989733311], ['0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 524.5602730745637]]
    [['0x6243d8cea23066d098a15582d81a598b4e8391f4', 129190.50613850323], ['0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 1316.4151091584395]]
    
    ```
    </details>

  ### 3: balance_of_lptoken_underlying(address, lptoken_address, block, blockchain)

  > Description: function returns balance of underlying tokens for given lp token

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Reflexer

    f3 = Reflexer.balance_of_lptoken_underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0xd6F3768E62Ef92a9798E5A8cEdD2b78907cEceF9', 'latest', Chain.ETHEREUM)

    print(f3)
    ```

    ```
    output:
    [['0x6243d8cea23066d098a15582d81a598b4e8391f4', 0.0], ['0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 0.0]]
    
    ```
    </details>


  ### 4: underlying(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0)

  > Description: funstion returns underlying tokens for given wallet and lp token on Reflexer protocol

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Reflexer

    
    f4 = Reflexer.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0xd6F3768E62Ef92a9798E5A8cEdD2b78907cEceF9', 'latest', Chain.ETHEREUM)

    print(f4)
    ```

    ```
    output:
    [['0x6243d8cea23066d098a15582d81a598b4e8391f4', 51479.35989733311], ['0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 524.5602730745637]]
    
    ```
    </details>

  </details>

- <details><summary><b>Sushiswap</b></summary>

  # Sushiswap

  ## Defined in Sushiswap.py

  ### 1: get_chef_contract(web3, block, blockchain, v1=False)

  > Description: function returns chef contract object for given blockchain

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import SushiSwap

    web3 = get_node(Chain.ETHEREUM, 'latest', 0)

    f1 = SushiSwap.get_chef_contract(web3, 'latest', Chain.ETHEREUM)

    print(f1)


    ```

    ```
    output: <web3._utils.datatypes.Contract object at 0x7fd83f1167d0>
    

    ```
    </details>



  ### 2: get_pool_info(web3, lptoken_address, block, blockchain, use_db=True)

  > Description: function returns pool info for given lp token

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import SushiSwap

    web3 = get_node(Chain.ETHEREUM, 'latest', 0)

    f2 = SushiSwap.get_pool_info(web3, '0x06da0fd433C1A5d7a4faa01111c044910A184553', 'latest', Chain.ETHEREUM)

    print(f2)

    ```

    ```
    output: 
    {'chef_contract': <web3._utils.datatypes.Contract object at 0x7f9f8e17e5f0>, 'pool_info': {'poolId': 0, 'allocPoint': 3000}, 'totalAllocPoint': 960240}
    

    ```
    </details>


  ### 3: get_lptoken_data(lptoken_address, block, blockchain, web3=None, execution=1, index=0)

  > Description: function returns lp roken data on Sushiswap protocol

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import SushiSwap

    f3 = SushiSwap.get_lptoken_data('0x397FF1542f962076d0BFE58eA045FfA2d347ACa0', 'latest', Chain.ETHEREUM)

    print(f3)


    ```

    ```
    output: 
    {'contract': <web3._utils.datatypes.Contract object at 0x7fa695232590>, 'decimals': 18, 'totalSupply': 319998674813332077, 'token0': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 'token1': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'reserves': [20433998700546, 14330389229987097177780, 1673554595], 'kLast': 292817359902509000116725434578391616, 'virtualTotalSupply': 3.199995668134856e+17}
    

    ```
    </details>


  ### 4: get_virtual_total_supply(lptoken_address, block, blockchain, web3=None, execution=1, index=0)

  > Description: function returns virtual total supply for given lp token


  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import SushiSwap

    f4 = SushiSwap.get_virtual_total_supply('0x397FF1542f962076d0BFE58eA045FfA2d347ACa0', 'latest', Chain.ETHEREUM)

    print(f4)

    ```

    ```
    output: 3.199995668134856e+17
    

    ```
    </details>


  ### 5: get_rewarder_contract(web3, block, blockchain, chef_contract, pool_id)

  > Description: function returns rewarder contracy for given chef contract


  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import SushiSwap

    web3 = get_node(Chain.ETHEREUM, 'latest', 0)

    f1 = SushiSwap.get_chef_contract(web3, 'latest', Chain.ETHEREUM)

    f5 = SushiSwap.get_rewarder_contract(web3, 'latest', Chain.ETHEREUM, f1, 1)

    print(f5)

    ```

    ```
    output: <web3._utils.datatypes.Contract object at 0x7f86c5aceaa0>
    

    ```
    </details>


  ### 6: get_sushi_rewards(web3, wallet, chef_contract, pool_id, block, blockchain, decimals=True)

  > Description: function returns sushi rewards for given wallet

    ```
    # Output:
    # 1 - Tuple: [sushi_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import SushiSwap

    web3 = get_node(Chain.ETHEREUM, 'latest', 0)

    f1 = SushiSwap.get_chef_contract(web3, 'latest', Chain.ETHEREUM)

    f6 = SushiSwap.get_sushi_rewards(web3, '0x849D52316331967b6fF1198e5E32A0eB168D039d', f1, 1, 'latest', Chain.ETHEREUM)

    print(f6)

    ```

    ```
    output: ['0x6B3595068778DD592e39A122f4f5a5cF09C90fE2', 0.0]
    

    ```
    </details>


  ### 7: get_rewards(web3, wallet, chef_contract, pool_id, block, blockchain, decimals=True)

  > Description: function retuens rewards for given wallet on Sushiswap protocol

    ```
    # Output:
    # 1 - List of Tuples: [reward_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import SushiSwap

    web3 = get_node(Chain.ETHEREUM, 'latest', 0)

    f1 = SushiSwap.get_chef_contract(web3, 'latest', Chain.ETHEREUM)

    f7 = SushiSwap.get_rewards(web3, '0x849D52316331967b6fF1198e5E32A0eB168D039d', f1, 1, 'latest', Chain.ETHEREUM)

    print(f7)

    ```

    ```
    output: [['0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B', 0.0]]
    

    ```
    </details>


  ### 8: get_all_rewards(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True, pool_info=None)

  > Description: function returns all the rewards for given wallet and lp token

    ```
    # 1 - List of Tuples: [reward_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import SushiSwap

    f8 = SushiSwap.get_all_rewards('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0x397FF1542f962076d0BFE58eA045FfA2d347ACa0', 'latest', Chain.ETHEREUM)

    print(f8)

    ```

    ```
    output: [['0x6B3595068778DD592e39A122f4f5a5cF09C90fE2', 0.0]]
    

    ```
    </details>

  ### 9: underlying(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True, reward=False)

  > Description: function returns undrlying tokens for given wallet and lptoken

    ```
    # Output: a list with 2 elements:
    # 1 - List of Tuples: [liquidity_token_address, balance, staked_balance]
    # 2 - List of Tuples: [reward_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import SushiSwap

    f9 = SushiSwap.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0x397FF1542f962076d0BFE58eA045FfA2d347ACa0', 'latest', Chain.ETHEREUM)

    print(f9)

    ```

    ```
    output: 
    [['0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 0.0, 0.0], ['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 0.0, 0.0]]
    

    ```
    </details>

  ### 10: pool_balances(lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True)

  > Description: function returns pool balances for given lp token 

    ```
    # Output: a list with 1 element:
    # 1 - List of Tuples: [liquidity_token_address, balance]
    ```
  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import SushiSwap

    f10 = SushiSwap.pool_balances('0x397FF1542f962076d0BFE58eA045FfA2d347ACa0', 'latest', Chain.ETHEREUM)

    print(f10)

    ```

    ```
    output: 
    [['0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 20198588.559822], ['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 14145.074969400264]]

    ```
    </details>


  ### 11: swap_fees(lptoken_address, block_start, block_end, blockchain, web3=None, execution=1, index=0, decimals=True)

  > description: function returns swap fees for given lp token and given block range

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import SushiSwap

    f11 = SushiSwap.swap_fees('0x397FF1542f962076d0BFE58eA045FfA2d347ACa0', 16392251, 'latest', Chain.ETHEREUM)

    print(f11)

    ```

    ```
    output:
    {'swaps': [{'block': 16393260, 'token': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 'amount': 0.349082604}, {'block': 16393261, 'token': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 'amount': 0.15}, {'block': 16393262, 'token': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 'amount': 59.582524791000004}, {'block': 16393330, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 7.5e-05}]}

    ```
    </details>

  ### 12: get_wallet_by_tx(lptoken_address, block, blockchain, web3=None, execution=1, index=0, signature=DEPOSIT_EVENT_SIGNATURE)

  > Description: function returns wallet by signature

    ```
    # 'signature' = signature of the type of transaction that will be searched for
    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import SushiSwap

    f12 = SushiSwap.get_wallet_by_tx('0x397FF1542f962076d0BFE58eA045FfA2d347ACa0', 'latest', Chain.ETHEREUM)

    print(f12)

    ```

    ```
    output: None
    ```
    </details>

  ### 13: get_rewards_per_unit(lptoken_address, blockchain, web3=None, execution=1, index=0, block='latest')

  > Description: function returns rewards per unit for given lp token

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import SushiSwap

    f13 = SushiSwap.get_rewards_per_unit('0x397FF1542f962076d0BFE58eA045FfA2d347ACa0', Chain.ETHEREUM)

    print(f13)
    ```

    ```
    output: 
    [{'sushi_address': '0x6B3595068778DD592e39A122f4f5a5cF09C90fE2', 'sushiPerBlock': 7.81054736315921e+17}]
    ```
    </details>


  ### 14: update_db()

  > Description: function updates the db
    

  </details>

- <details><summary><b>Swapr</b></summary>

  # Swapr

  ## Defined in Swapr.py

  ### 1: get_staking_rewards_contract(web3, block, blockchain)

  > Description: function returns stacking rewards contract


  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Swapr

    web3 = get_node(Chain.ETHEREUM, 'latest', 0)

    f1 = Swapr.get_staking_rewards_contract(web3, 'latest', Chain.ETHEREUM)

    print(f1)

    ```

    ```
    output: 
    <web3._utils.datatypes.Contract object at 0x7fecf9dd2710>

    ```
    </details>


  ### 2: get_distribution_contracts(web3, lptoken_address, staking_rewards_contract, campaigns, block, blockchain)

  > Description: function returns disctribution contracts for given lp token

  ** Help Needed **

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Swapr

    web3 = get_node(Chain.ETHEREUM, 'latest', 0)

    f1 = Swapr.get_staking_rewards_contract(web3, 'latest', Chain.ETHEREUM)

    f2 = Swapr.get_distribution_contracts(web3, '0x7515Be43D16f871588ADc135d58a9c30A71Eb34F', f1, 1, 'latest', Chain.ETHEREUM)

    print(f2)

    ```

    ```
    output: 
    

    ```
    </details>

  ### 3: get_lptoken_data(lptoken_address, block, blockchain, web3=None, execution=1, index=0)

  > Description: function returns lp token data

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Swapr

    f3 = Swapr.get_lptoken_data('0x7515Be43D16f871588ADc135d58a9c30A71Eb34F', 'latest', Chain.ETHEREUM)

    print(f3)

    ```

    ```
    output: 
    {'contract': <web3._utils.datatypes.Contract object at 0x7fc6a413e6e0>, 'decimals': 18, 'totalSupply': 8788345579684989628399, 'token0': '0x6B175474E89094C44Da98b954EedeAC495271d0F', 'token1': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'reserves': [367338598438067871621998, 257554709560248473048, 1673559707], 'kLast': 0, 'virtualTotalSupply': 1.0546014695621988e+22}
    

    ```
    </details>


  ### 4: get_all_rewards(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True, campaigns=1, distribution_contracts=[])

  > Description: function returns all rewards for given wallet and lp token

    ```
    # Output:
    # 1 - List of Tuples: [reward_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Swapr

    f4 = Swapr.get_all_rewards('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0x7515Be43D16f871588ADc135d58a9c30A71Eb34F', 'latest', Chain.ETHEREUM)

    print(f4)

    ```

    ```
    output: None

    ```
    </details>

  ### 5: underlying(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True, reward=False, campaigns=1)

  > Description: function returns underlying tokens for given wallet and lp token

    ```
    # Output: a list with 2 elements:
    # 1 - List of Tuples: [liquidity_token_address, balance, staked_balance]
    # 2 - List of Tuples: [reward_token_address, balance]

    ```

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Swapr

    f5 = Swapr.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0x7515Be43D16f871588ADc135d58a9c30A71Eb34F', 'latest', Chain.ETHEREUM)

    print(f5)

    ```

    ```
    output: None

    ```
    </details>


  ### 6: pool_balances(lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True)

  > Description: function returns pool balance for given lp token

    ```
    # Output: a list with 1 element:
    # 1 - List of Tuples: [liquidity_token_address, balance]
    ```
  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Swapr

    f6 = Swapr.pool_balances('0x7515Be43D16f871588ADc135d58a9c30A71Eb34F', 'latest', Chain.ETHEREUM)

    print(f6)

    ```

    ```
    output: 
    [['0x6B175474E89094C44Da98b954EedeAC495271d0F', 367338.5984380679], ['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 257.55470956024845]]

    ```
    </details>

  ### 7: swap_fees(lptoken_address, block_start, block_end, blockchain, web3=None, execution=1, index=0, decimals=True)

  > Description: function returns swap fees for given lp token and block range


  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Swapr

    f7 = Swapr.swap_fees('0x7515Be43D16f871588ADc135d58a9c30A71Eb34F', 16392504, 'latest', Chain.ETHEREUM)

    print(f7)

    ```

    ```
    output: 
    {'swaps': [{'block': 16392554, 'token': '0x6B175474E89094C44Da98b954EedeAC495271d0F', 'amount': 0.3533967616636148}, {'block': 16392693, 'token': '0x6B175474E89094C44Da98b954EedeAC495271d0F', 'amount': 0.8042712308268711}, {'block': 16392942, 'token': '0x6B175474E89094C44Da98b954EedeAC495271d0F', 'amount': 1.3125}, {'block': 16392986, 'token': '0x6B175474E89094C44Da98b954EedeAC495271d0F', 'amount': 1.12284669760275}, {'block': 16393054, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 4.3810185944715885e-05}, {'block': 16393185, 'token': '0x6B175474E89094C44Da98b954EedeAC495271d0F', 'amount': 0.13697197835428987}, {'block': 16393190, 'token': '0x6B175474E89094C44Da98b954EedeAC495271d0F', 'amount': 0.1027289837657174}, {'block': 16393338, 'token': '0x6B175474E89094C44Da98b954EedeAC495271d0F', 'amount': 0.2434762712795}, {'block': 16393463, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 0.00035039806149557873}, {'block': 16393467, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 0.000173850319209059}]}
    
    ```
    </details>

  </details>

- <details><summary><b>Symmetric</b></summary>

  # Symmetric

  ## Defined in Symmetric.py

  ### 1: get_vault_contract(web3, block, blockchain)

  > Description: function returns valut contract for given blockchain


  - <details><summary><b>Example</b></summary>

    ```

    from defyes import *

    from defyes.functions import *

    from defyes import Symmetric

    web3 = get_node(Chain.GNOSIS, 'latest', 0)

    f1 = Symmetric.get_vault_contract(web3, 'latest', Chain.GNOSIS)

    print(f1)


    ```

    ```
    output: <web3._utils.datatypes.Contract object at 0x7fa761bb27a0>

    ```
    </details>


  ### 2: get_chef_contract(web3, block, blockchain)

  > Description: function returns chef contract for given blockchain on Symmetric protocol


  - <details><summary><b>Example</b></summary>

    ```

    from defyes import *

    from defyes.functions import *

    from defyes import Symmetric

    web3 = get_node(Chain.GNOSIS, 'latest', 0)

    f2 = Symmetric.get_chef_contract(web3, 'latest', Chain.GNOSIS)

    print(f2)

    ```

    ```
    output: <web3._utils.datatypes.Contract object at 0x7fa9fbafe830>

    ```
    </details>


  ### 3: get_pool_info(web3, lptoken_address, block, blockchain)

  > Description: function returns pool info for given lp token


  - <details><summary><b>Example</b></summary>

    ```

    from defyes import *

    from defyes.functions import *

    from defyes import Symmetric

    web3 = get_node(Chain.GNOSIS, 'latest', 0)

    f3 = Symmetric.get_pool_info(web3, '0x8B78873717981F18C9B8EE67162028BD7479142b', 'latest', Chain.GNOSIS)

    print(f3)

    ```

    ```
    output: 
    {'chef_contract': <web3._utils.datatypes.Contract object at 0x7f560927a830>, 'pool_info': {'poolId': 0, 'allocPoint': 0}, 'totalAllocPoint': 98}

    ```
    </details>


  ### 4: get_lptoken_data(lptoken_address, block, blockchain, web3=None, execution=1, index=0)

  > Description: function returns lp token data for given lp token

  - <details><summary><b>Example</b></summary>

    ```

    from defyes import *

    from defyes.functions import *

    from defyes import Symmetric

    web3 = get_node(Chain.GNOSIS, 'latest', 0)

    f4 = Symmetric.get_lptoken_data('0x8B78873717981F18C9B8EE67162028BD7479142b', 'latest', Chain.GNOSIS)

    print(f4)

    ```

    ```
    output: 
    {'contract': <web3._utils.datatypes.Contract object at 0x7f1285a66740>, 'poolId': b'\x8bx\x877\x17\x98\x1f\x18\xc9\xb8\xeeg\x16 (\xbdty\x14+\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 'decimals': 18, 'totalSupply': 612664746701529997}

    ```
    </details>


  ### 5: get_rewarder_contract(web3, block, blockchain, chef_contract, pool_id)

  > Description: function returns rewarder contract for given chef contract and pool id

  - <details><summary><b>Example</b></summary>

    ```

    from defyes import *

    from defyes.functions import *

    from defyes import Symmetric

    web3 = get_node(Chain.GNOSIS, 'latest', 0)

    f2 = Symmetric.get_chef_contract(web3, 'latest', Chain.GNOSIS)

    f5 = Symmetric.get_rewarder_contract(web3, 'latest', Chain.GNOSIS, f2, 0)

    print(f5)

    ```

    ```
    output: <web3._utils.datatypes.Contract object at 0x7f69a936aaa0>

    ```
    </details>


  ### 6: get_symm_rewards(web3, wallet, chef_contract, pool_id, block, blockchain, decimals=True)

  > Description: function returns symm rewards for given wallet and chef contract

    ```
    # Output:
    # 1 - Tuple: [symm_token_address, balance]
    ```
  - <details><summary><b>Example</b></summary>

    ```

    from defyes import *

    from defyes.functions import *

    from defyes import Symmetric

    web3 = get_node(Chain.GNOSIS, 'latest', 0)

    f2 = Symmetric.get_chef_contract(web3, 'latest', Chain.GNOSIS)

    f6 = Symmetric.get_symm_rewards(web3, '0x849D52316331967b6fF1198e5E32A0eB168D039d', f2, 0, 'latest', Chain.GNOSIS, 0)

    print(f6)

    ```

    ```
    output: 
    ['0xC45b3C1c24d5F54E7a2cF288ac668c74Dd507a84', 0.0]

    ```
    </details>


  ### 7: get_rewards(web3, wallet, chef_contract, pool_id, block, blockchain, decimals=True)

  > Description: function returns rewards for given wallet and chef contract and pool id

    ```
    # Output:
    # 1 - List of Tuples: [reward_token_address, balance]
    ```
  - <details><summary><b>Example</b></summary>

    ```

    from defyes import *

    from defyes.functions import *

    from defyes import Symmetric

    web3 = get_node(Chain.GNOSIS, 'latest', 0)

    f2 = Symmetric.get_chef_contract(web3, 'latest', Chain.GNOSIS)

    f7 = Symmetric.get_rewards(web3, '0x849D52316331967b6fF1198e5E32A0eB168D039d', f2, 0, 'latest', Chain.GNOSIS, 0)

    print(f7)

    ```

    ```
    output: 
    [['0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb', 0.0]]

    ```
    </details>


  ### 8: get_all_rewards(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True, pool_info=None)

  > Description: function returns all rewards for given wallet on given lp token fo Symmetric protocol

    ```
    # Output:
    # 1 - List of Tuples: [reward_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```

    from defyes import *

    from defyes.functions import *

    from defyes import Symmetric

    f8 = Symmetric.get_all_rewards('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0x8B78873717981F18C9B8EE67162028BD7479142b', 'latest', Chain.GNOSIS)

    print(f8)


    ```

    ```
    output: 
    [['0xC45b3C1c24d5F54E7a2cF288ac668c74Dd507a84', 0.0], ['0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb', 0.0]]
    

    ```
    </details>


  ### 9: underlying(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True, reward=False)

  > Description: function returns underlying tokens for given wallet and lp token on Symmetric protocol

    ```
    # Output: a list with 2 elements:
    # 1 - List of Tuples: [liquidity_token_address, balance, staked_balance]
    # 2 - List of Tuples: [reward_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```

    from defyes import *

    from defyes.functions import *

    from defyes import Symmetric

    f9 = Symmetric.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0x8B78873717981F18C9B8EE67162028BD7479142b', 'latest', Chain.GNOSIS)

    print(f9)


    ```

    ```
    output: 
    [['0xC45b3C1c24d5F54E7a2cF288ac668c74Dd507a84', 0.0, 0.0], ['0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 0.0, 0.0]]

    ```
    </details>


  ### 10: pool_balances(lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True)

  > description: function returns pool balances for given lp token on Symmetric protocol

    ```
    # Output: a list with 1 element
    # 1 - List of Tuples: [liquidity_token_address, balance]
    ```

  - <details><summary><b>Example</b></summary>

    ```

    from defyes import *

    from defyes.functions import *

    from defyes import Symmetric

    f10 = Symmetric.pool_balances('0x8B78873717981F18C9B8EE67162028BD7479142b', 'latest', Chain.GNOSIS)

    print(f10)

    ```

    ```
    output: 
    [['0xC45b3C1c24d5F54E7a2cF288ac668c74Dd507a84', 0.5824447991127851], ['0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 0.023928716865637658]]
    
    ```
    </details>

  ### 11: get_rewards_per_unit(lptoken_address, blockchain, web3=None, execution=1, index=0, block='latest')

  > Description: function returns rewards per units for given lp token

  - <details><summary><b>Example</b></summary>

    ```

    from defyes import *

    from defyes.functions import *

    from defyes import Symmetric

    f11 = Symmetric.get_rewards_per_unit('0x8B78873717981F18C9B8EE67162028BD7479142b', Chain.GNOSIS)

    print(f11)

    ```

    ```
    output: 
    [{'symm_address': '0xC45b3C1c24d5F54E7a2cF288ac668c74Dd507a84', 'symmPerSecond': 0.0}, {'reward_address': '0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb', 'rewardPerSecond': 0.0}]
    
    ```
    </details>

  ### 12: update_db()

  > Description: function updates the db

  ### 13: underlyingv1(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True, reward=False)

  > Description: function returns underlying tokens for given wallet and lp token for symmetric v1 protocol

    ```
    # Output: a list with 2 elements:
    # 1 - List of Tuples: [liquidity_token_address, balance, staked_balance]
    # 2 - List of Tuples: [reward_token_address, balance]
    ```
  - <details><summary><b>Example</b></summary>

    ```

    from defyes import *

    from defyes.functions import *

    from defyes import Symmetric

    f13 = Symmetric.underlyingv1('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0x8B78873717981F18C9B8EE67162028BD7479142b', 'latest', Chain.GNOSIS)

    print(f13)

    ```

    ```
    output: 
    0
    612664746701529997
    [['0xC45b3C1c24d5F54E7a2cF288ac668c74Dd507a84', 0.0, 0.0], ['0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 0.0, 0.0]]

    
    ```
    </details>


  ### 14: swap_fees(lptoken_address, block_start, block_end, blockchain, web3=None, execution=1, index=0, decimals=True)

  > Description: function returns swap fees for given lp token for given range

  - <details><summary><b>Example</b></summary>

    ```

    from defyes import *

    from defyes.functions import *

    from defyes import Symmetric

    f14 = Symmetric.swap_fees('0x65b0e9418e102a880c92790f001a9c5810b0ef32', 25928795, 'latest', Chain.GNOSIS)

    print(f14)

    ```

    ```
    output: 
    {'swaps': [{'block': 25930778, 'token': '0xb7D311E2Eb55F2f68a9440da38e7989210b9A05e', 'amount': 0.010421660802460526}, {'block': 25930780, 'token': '0xb7D311E2Eb55F2f68a9440da38e7989210b9A05e', 'amount': 0.007520257123154599}, {'block': 25930784, 'token': '0xb7D311E2Eb55F2f68a9440da38e7989210b9A05e', 'amount': 0.008243855399208456}, {'block': 25930789, 'token': '0xb7D311E2Eb55F2f68a9440da38e7989210b9A05e', 'amount': 0.007877870087106005}, {'block': 25930797, 'token': '0xb7D311E2Eb55F2f68a9440da38e7989210b9A05e', 'amount': 0.006428455971430291}, {'block': 25930802, 'token': '0xb7D311E2Eb55F2f68a9440da38e7989210b9A05e', 'amount': 0.006066430265895466}, {'block': 25930804, 'token': '0xb7D311E2Eb55F2f68a9440da38e7989210b9A05e', 'amount': 0.006064083055418988}, {'block': 25930810, 'token': '0xb7D311E2Eb55F2f68a9440da38e7989210b9A05e', 'amount': 0.006061810233426429}, {'block': 25930831, 'token': '0xb7D311E2Eb55F2f68a9440da38e7989210b9A05e', 'amount': 0.006061737207627279}, {'block': 25930833, 'token': '0xb7D311E2Eb55F2f68a9440da38e7989210b9A05e', 'amount': 0.006059392721465463}]}

    
    ```
    </details>

  </details>

- <details><summary><b>UniswapV3</b></summary>

  # UniswapV3

  ## Defined in UniswapV3.py


  ### 1: get_rate_uniswap_v3(token_src, token_dst, block, blockchain, web3=None, execution=1, index=0, fee=100)

  > Description: function returns 

  *** Help Needed ***

  - <details><summary><b>Example</b></summary>

    ```
  

    ```

    ```
    output: 
    
    
    ```
    </details>


  ### 2: underlying(wallet, nftid, block, blockchain, web3=None, execution=1, index=0, decimals=True)

  > Description: function returns underlying tokens for given wallter and nft id

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import UniswapV3

    f2 = UniswapV3.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', 214704, 'latest', Chain.ETHEREUM)

    print(f2)

    ```

    ```
    output: 
    [['0x6810e776880C02933D47DB1b9fc05908e5386b96', 0], ['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 0]]
    
    
    ```
    </details>

  ### 3: allnfts(wallet, block, blockchain, web3=None, execution=1, index=0)

  > Description: function returns all nfts for given wallet on UniswapV3 protocol

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import UniswapV3

    f3 = UniswapV3.allnfts('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', Chain.ETHEREUM)

    print(f3)

    ```

    ```
    output: [185085, 186529, 189493, 214704, 214707, 214716, 218573, 220361, 217714, 286920, 339884, 346143, 358770]
    
    
    ```
    </details>


  ### 3: get_fee(nftid, block, blockchain, web3=None, execution=1, index=0, decimals=True)

  > Description: function returns fees for given nft id on UniswapV3 protocol


  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import UniswapV3

    f4 = UniswapV3.get_fee(346143, 'latest', Chain.ETHEREUM)

    print(f4)

    ```

    ```
    output: 
    [['0x6810e776880C02933D47DB1b9fc05908e5386b96', 0.0], ['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 0.0]]
    
    
    ```
    </details>


  </details>


- <details><summary><b>Unit</b></summary>

  # Unit

  ## Defined in Unit.py


  ### 1: get_vault_address(blockchain)

  > Description: function returns vault address for given blockchain

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Unit

    f1 = Unit.get_vault_address(Chain.ETHEREUM)

    print(f1)

    ```

    ```
    output: 0xb1cFF81b9305166ff1EFc49A129ad2AfCd7BCf19
    

    ```
    </details>


  ### 2: get_cdp_registry_address(blockchain)

  > Description: function returns cdp registry address for given blockchain

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Unit

    f2 = Unit.get_cdp_registry_address(Chain.ETHEREUM)

    print(f2)

    ```

    ```
    output: 0x1a5Ff58BC3246Eb233fEA20D32b79B5F01eC650c
    

    ```
    </details>

  ### 3: get_cdp_manager_address(blockchain)

  > Description: function returns cdp manager for given blockchain

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Unit

    f3 = Unit.get_cdp_manager_address(Chain.ETHEREUM)

    print(f3)

    ```

    ```
    output: 0x69FB4D4e3404Ea023F940bbC547851681e893a91

    ```
    </details>


  ### 4: get_cdp_viewer_address(blockchain)

  > Description: function retunrs cdp viewer address for given blockchain


  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Unit

    f4 = Unit.get_cdp_viewer_address(Chain.ETHEREUM)

    print(f4)

    ```

    ```
    output: 0x68AF7bD6F3e2fb480b251cb1b508bbb406E8e21D
    
    ```
    </details>

  ### 5: get_cdp_viewer_data(wallet, collateral_address, block, blockchain, web3=None, execution=1, index=0, decimals=True)

  > Description: function returns cdp viewer data for given wallet and collateral address

  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Unit

    f5 = Unit.get_cdp_viewer_data('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'latest', Chain.ETHEREUM)

    print(f5)

    ```

    ```
    output: {}
    
    ```
    </details>

  ### 6: get_cdp_data(wallet, collateral_address, block, blockchain, web3=None, execution=1, index=0, decimals=True)

  > Description: function returns cdp data for given wallet and collateral address


  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Unit

    f6 = Unit.get_cdp_data('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'latest', Chain.ETHEREUM)

    print(f6)

    ```

    ```
    output: {}
    
    ```
    </details>


  ### 7: underlying(wallet, block, blockchain, web3=None, execution=1, index=0, decimals=True)

  > Description: function returns underlying tokens for given wallet on Unit protocol

    ```
    # Output: a list with N elements, where N = number of CDPs for the wallet:
    # 1 - List of Tuples: [[collateral_addressN, collateral_amountN], [debt_addressN, -debt_amountN]]
    
    ```
  - <details><summary><b>Example</b></summary>

    ```
    from defyes import *

    from defyes.functions import *

    from defyes import Unit

    f7 = Unit.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', Chain.ETHEREUM)

    print(f7)

    ```

    ```
    output: []
    
    ```
    </details>


  </details>

## Running the test

```
pip install -r requirements-dev.txt

pytest -vs tests/

```

## Building and distributing

```
pip install --upgrade build

python -m build

```


## 💙 Contributing

PR's are welcome !

Please open a pull request in dev branch if you want to contribute to this awesome protocols!

Found a Bug ? Create an Issue.



## Development

If it's possible, just use `make` witch gives you many shortcuts.  Otherwise try to mimic what it does by seeing
[Makefile](Makefile).

The easy way is to call `make`, which by default build the docker image with all the dependencies and install the git
pre-commit hook to encorage you to commit well formatted code.


### Build the docker image

Run `make build` to build the docker image used to following development workflows.

The default image name used is `defyes`. You could override it specify `make build image=...`.

The default `CONFIG_FILE` is defined as `config.json` from the current working directory.

Every time a command is executed using this image, all the repository directory is mounted at `/repo` which is also
the default current working directory inside the container. `.tmp` is mounted to `/tmp`, where the Internet
requests/responces cache lives by default. `/repo/.home` is defined as the `HOME` to keep bash and ipython
configurations and history across shell sessions.


### Install the pre-commit hook

To install or re-install the pre-commit hook, call `make install-pre-commit`. It'll copy the [.pre-commit](.pre-commit)
file into the `.git` directory, to check for [linting](#linting) every time you try to create a new git
commit.


### Linting

Linting is the process to check code format accomplishment.

From now on you shoud ensure linting before commiting code. To help you doing that, `make lint` just check the code
formatting.  It includes executing `black`, `isort` and `flake8` just in checking mode. If you want to apply `black`
and `isort` changes automatically to your working-copy code, use `make pretty`.

`flake8` just check the code, but it doesn't apply chages automatically. You shoud decide how to make the changes
yourself base on the `flake8` output. Anyway, many code formatting rules `flake8` checks are sanitized automatically
by `black`.

> To change the default path where the linter checks, you could specify `make lint path=...`.


### Testing

The short way is just calling `make test`, which runs all tests.

if you want to specify a non default `config.json`, just overrider the env like
```shell
make test CONFIG_FILE=...
```

To have more control see [below](#a-shell-inside-the-container).


### IPython

Run `make ipython` straight away or `make shell` and then `ipython`.


### A shell inside the container

If you prefer to have more control over linting, testing, or debugging, execute `make shell`.

`make shell` starts `bash` inside the container. Then, you can directly run `pytest`, `black`, `ipython`, etc.

`bash`, as well as `ipython`, keeps its command history ;)

`make shell` executes `bash` with the same user you called it (your own user). As the repo volume is mounted in
read-write mode inside the container, it's useful to have new files or modified files with the same user you own
instead of the root user. But, if you prefer to run it with the root user, call `make rootshell` instead.

> `make` is always intended to be used outside the container.

Some examples of calling `pytest` inside the container could be:

```shell
pytest -v
```
```shell
pytest -vvs tests/test_azuro.py
```
```shell
pytest tests/test_azuro.py --pdb -k deposit
```

> The `.home` directory is git ignored to prevent committing command history among other things, except for the
> `.home/.bashrc` which you can edit and commit changes on it to define new bash command aliases or change the prompt.


## 💖 Like this project ?

Leave a ⭐ If you think this project is cool.

Follow use on [twitter](https://twitter.com/karpatkey)
