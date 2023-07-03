# Symmetric

## Defined in Symmetric.py

### 1: get_vault_contract(web3, block, blockchain)

> Description: function returns valut contract for given blockchain


- <details><summary><b>Example</b></summary>

  ```

  from defyes import *

  from defyes.functions import *

  from defyes import Symmetric

  web3 = get_node(XDAI, 'latest', 0)

  f1 = Symmetric.get_vault_contract(web3, 'latest', XDAI)

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

  web3 = get_node(XDAI, 'latest', 0)

  f2 = Symmetric.get_chef_contract(web3, 'latest', XDAI)

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

  web3 = get_node(XDAI, 'latest', 0)

  f3 = Symmetric.get_pool_info(web3, '0x8B78873717981F18C9B8EE67162028BD7479142b', 'latest', XDAI)

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

  web3 = get_node(XDAI, 'latest', 0)

  f4 = Symmetric.get_lptoken_data('0x8B78873717981F18C9B8EE67162028BD7479142b', 'latest', XDAI)

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

  web3 = get_node(XDAI, 'latest', 0)

  f2 = Symmetric.get_chef_contract(web3, 'latest', XDAI)

  f5 = Symmetric.get_rewarder_contract(web3, 'latest', XDAI, f2, 0)

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

  web3 = get_node(XDAI, 'latest', 0)

  f2 = Symmetric.get_chef_contract(web3, 'latest', XDAI)

  f6 = Symmetric.get_symm_rewards(web3, '0x849D52316331967b6fF1198e5E32A0eB168D039d', f2, 0, 'latest', XDAI, 0)

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

  web3 = get_node(XDAI, 'latest', 0)

  f2 = Symmetric.get_chef_contract(web3, 'latest', XDAI)

  f7 = Symmetric.get_rewards(web3, '0x849D52316331967b6fF1198e5E32A0eB168D039d', f2, 0, 'latest', XDAI, 0)

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

  f8 = Symmetric.get_all_rewards('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0x8B78873717981F18C9B8EE67162028BD7479142b', 'latest', XDAI)

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

  f9 = Symmetric.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0x8B78873717981F18C9B8EE67162028BD7479142b', 'latest', XDAI)

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

  f10 = Symmetric.pool_balances('0x8B78873717981F18C9B8EE67162028BD7479142b', 'latest', XDAI)

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

  f11 = Symmetric.get_rewards_per_unit('0x8B78873717981F18C9B8EE67162028BD7479142b', XDAI)

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

  f13 = Symmetric.underlyingv1('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0x8B78873717981F18C9B8EE67162028BD7479142b', 'latest', XDAI)

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

  f14 = Symmetric.swap_fees('0x65b0e9418e102a880c92790f001a9c5810b0ef32', 25928795, 'latest', XDAI)

  print(f14)

  ```

  ```
  output: 
  {'swaps': [{'block': 25930778, 'token': '0xb7D311E2Eb55F2f68a9440da38e7989210b9A05e', 'amount': 0.010421660802460526}, {'block': 25930780, 'token': '0xb7D311E2Eb55F2f68a9440da38e7989210b9A05e', 'amount': 0.007520257123154599}, {'block': 25930784, 'token': '0xb7D311E2Eb55F2f68a9440da38e7989210b9A05e', 'amount': 0.008243855399208456}, {'block': 25930789, 'token': '0xb7D311E2Eb55F2f68a9440da38e7989210b9A05e', 'amount': 0.007877870087106005}, {'block': 25930797, 'token': '0xb7D311E2Eb55F2f68a9440da38e7989210b9A05e', 'amount': 0.006428455971430291}, {'block': 25930802, 'token': '0xb7D311E2Eb55F2f68a9440da38e7989210b9A05e', 'amount': 0.006066430265895466}, {'block': 25930804, 'token': '0xb7D311E2Eb55F2f68a9440da38e7989210b9A05e', 'amount': 0.006064083055418988}, {'block': 25930810, 'token': '0xb7D311E2Eb55F2f68a9440da38e7989210b9A05e', 'amount': 0.006061810233426429}, {'block': 25930831, 'token': '0xb7D311E2Eb55F2f68a9440da38e7989210b9A05e', 'amount': 0.006061737207627279}, {'block': 25930833, 'token': '0xb7D311E2Eb55F2f68a9440da38e7989210b9A05e', 'amount': 0.006059392721465463}]}

  
  ```
  </details>

