# Agave

## Defined in Agave.py


### 1: `get_reserves_tokens(pdp_contract, block)`

> Description: function returns reserved tokens for agave protocol

- <details><summary><b>Example</b></summary>

  ```
  from defyes.constants import XDAI
  from defyes import Agave

  pdp_contract = Agave.get_contract(Agave.PDP_XDAI, XDAI)
  tokens = Agave.get_reserves_tokens(pdp_contract, 'latest')
  print(tokens)
  ```

  ```
  output:
  ['0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83', '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', '0xE2e73A1c69ecF83F464EFCE6A5be353a37cA09b2', '0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb', '0x8e5bBbb09Ed1ebdE8674Cda39A0c169401db4252', '0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1', '0x21a42669643f45Bc0e086b8Fc2ed70c23D67509d', '0x4ECaBa5870353805a9F068101A40E0f32ed605C6']
  ```
  </details>

### 2: `get_reserves_tokens_balances(web3, wallet, block, blockchain, decimals=True)`

> Description: function returns reserved token balances for given wallet address

- <details><summary><b>Example</b></summary>

  ```
  from defyes.constants import XDAI
  from defyes.functions import get_node
  from defyes import Agave

  web3 = get_node(XDAI, 'latest', 0)
  f2 = Agave.get_reserves_tokens_balances(web3, '0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', XDAI)

  print(f2)

  ```

  ```
  output: []
  ```
  </details>


### 3: `get_data(wallet, block, blockchain, execution=1, web3=None, index=1, decimals=True)`

> Description: function returns agave data for given wallet address

- <details><summary><b>Example</b></summary>

  ```
  from defyes.constants import XDAI
  from defyes import Agave

  f3 = Agave.get_data('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', XDAI)
  print(f3)
  ```

  ```
  output: None
  
  ```
  </details>

### 4: `get_all_rewards(wallet, block, blockchain, execution=1, web3=None, index=0, decimals=True)`

> Description: function returns all rewards for given wallet on agave protocol

- <details><summary><b>Example</b></summary>

  ```
  from defyes.constants import XDAI
  from defyes import Agave

  f4 = Agave.get_all_rewards('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', XDAI)
  print(f4)
  ```

  ```
  output: [['0x3a97704a1b25F08aa230ae53B352e2e72ef52843', 0.0]]
  ```
  </details>

### 5: `underlying(wallet, block, blockchain, execution=1, web3=None, index=0, decimals=True, reward=False)`

FIXME: this function does not exist anymore

> Description: function returns underlying tokens for given wallet from agave protocol

- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import Agave

  f5 = Agave.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', XDAI, reward=True)

  print(f5)


  ```

  ```
  output: [[], [['0x3a97704a1b25F08aa230ae53B352e2e72ef52843', 0.0]]]
  
  ```
  </details>
