# Functions

## Defined in functions.py


### 1: get_node(blockchain)

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

### 11: balance_of(address, contract_address, block, blockchain, web3=None, decimals=True)

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

### 12: total_supply(token_address, block, blockchain, web3=None, decimals=True)

> Description: fucntion returns total suppy for a given token contract address

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

### 13: get_decimals(token_address, blockchain, web3=None, block='latest')

> Description: function returns decimals for given token address


### 14: get_symbol(token_address, blockchain, web3=None, block='latest') -> str

> Description: function returns symbol for given toke contract address

### 15: get_contract_abi(contract_address, blockchain)

> fucntion returns abi for given contract address

### 16: get_contract(contract_address, blockchain, web3=None, abi=None, block='latest')

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
  # a = get_contract_abi('0xdc31ee1784292379fbb2964b3b9c4124d8f89c60', GOERLI)

  # print(a)

  b = get_contract_proxy_abi('0xdc31ee1784292379fbb2964b3b9c4124d8f89c60', '0xe2E52C2D0D64209b8DD1854371A4C673c13448f0', GOERLI)

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


