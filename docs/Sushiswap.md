# Sushiswap

## Defined in Sushiswap.py

### 1: get_chef_contract(web3, block, blockchain, v1=False)

> Description: function returns chef contract object for given blockchain

- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import SushiSwap

  web3 = get_node(ETHEREUM, 'latest', 0)

  f1 = SushiSwap.get_chef_contract(web3, 'latest', ETHEREUM)

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

  web3 = get_node(ETHEREUM, 'latest', 0)

  f2 = SushiSwap.get_pool_info(web3, '0x06da0fd433C1A5d7a4faa01111c044910A184553', 'latest', ETHEREUM)

  print(f2)

  ```

  ```
  output: 
  {'chef_contract': <web3._utils.datatypes.Contract object at 0x7f9f8e17e5f0>, 'pool_info': {'poolId': 0, 'allocPoint': 3000}, 'totalAllocPoint': 960240}
  

  ```
  </details>


### 3: get_lptoken_data(lptoken_address, block, blockchain, web3=None)

> Description: function returns lp roken data on Sushiswap protocol

- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import SushiSwap

  f3 = SushiSwap.get_lptoken_data('0x397FF1542f962076d0BFE58eA045FfA2d347ACa0', 'latest', ETHEREUM)

  print(f3)


  ```

  ```
  output: 
  {'contract': <web3._utils.datatypes.Contract object at 0x7fa695232590>, 'decimals': 18, 'totalSupply': 319998674813332077, 'token0': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 'token1': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'reserves': [20433998700546, 14330389229987097177780, 1673554595], 'kLast': 292817359902509000116725434578391616, 'virtualTotalSupply': 3.199995668134856e+17}
  

  ```
  </details>


### 4: get_virtual_total_supply(lptoken_address, block, blockchain, web3=None)

> Description: function returns virtual total supply for given lp token


- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import SushiSwap

  f4 = SushiSwap.get_virtual_total_supply('0x397FF1542f962076d0BFE58eA045FfA2d347ACa0', 'latest', ETHEREUM)

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

  web3 = get_node(ETHEREUM, 'latest', 0)

  f1 = SushiSwap.get_chef_contract(web3, 'latest', ETHEREUM)

  f5 = SushiSwap.get_rewarder_contract(web3, 'latest', ETHEREUM, f1, 1)

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

  web3 = get_node(ETHEREUM, 'latest', 0)

  f1 = SushiSwap.get_chef_contract(web3, 'latest', ETHEREUM)

  f6 = SushiSwap.get_sushi_rewards(web3, '0x849D52316331967b6fF1198e5E32A0eB168D039d', f1, 1, 'latest', ETHEREUM)

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

  web3 = get_node(ETHEREUM, 'latest', 0)

  f1 = SushiSwap.get_chef_contract(web3, 'latest', ETHEREUM)

  f7 = SushiSwap.get_rewards(web3, '0x849D52316331967b6fF1198e5E32A0eB168D039d', f1, 1, 'latest', ETHEREUM)

  print(f7)

  ```

  ```
  output: [['0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B', 0.0]]
  

  ```
  </details>


### 8: get_all_rewards(wallet, lptoken_address, block, blockchain, web3=None, decimals=True, pool_info=None)

> Description: function returns all the rewards for given wallet and lp token

  ```
  # 1 - List of Tuples: [reward_token_address, balance]
  ```

- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import SushiSwap

  f8 = SushiSwap.get_all_rewards('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0x397FF1542f962076d0BFE58eA045FfA2d347ACa0', 'latest', ETHEREUM)

  print(f8)

  ```

  ```
  output: [['0x6B3595068778DD592e39A122f4f5a5cF09C90fE2', 0.0]]
  

  ```
  </details>

### 9: underlying(wallet, lptoken_address, block, blockchain, web3=None, decimals=True, reward=False)

> Description: fucntion returns undrlying tokens for given wallet and lptoken

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

  f9 = SushiSwap.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0x397FF1542f962076d0BFE58eA045FfA2d347ACa0', 'latest', ETHEREUM)

  print(f9)

  ```

  ```
  output: 
  [['0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 0.0, 0.0], ['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 0.0, 0.0]]
  

  ```
  </details>

### 10: pool_balances(lptoken_address, block, blockchain, web3=None, decimals=True)

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

  f10 = SushiSwap.pool_balances('0x397FF1542f962076d0BFE58eA045FfA2d347ACa0', 'latest', ETHEREUM)

  print(f10)

  ```

  ```
  output: 
  [['0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 20198588.559822], ['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 14145.074969400264]]

  ```
  </details>


### 11: swap_fees(lptoken_address, block_start, block_end, blockchain, web3=None, decimals=True)

> description: function returns swap fees for given lp token and given block range

- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import SushiSwap

  f11 = SushiSwap.swap_fees('0x397FF1542f962076d0BFE58eA045FfA2d347ACa0', 16392251, 'latest', ETHEREUM)

  print(f11)

  ```

  ```
  output:
  {'swaps': [{'block': 16393260, 'token': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 'amount': 0.349082604}, {'block': 16393261, 'token': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 'amount': 0.15}, {'block': 16393262, 'token': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 'amount': 59.582524791000004}, {'block': 16393330, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 7.5e-05}]}

  ```
  </details>

### 12: get_wallet_by_tx(lptoken_address, block, blockchain, web3=None, signature=DEPOSIT_EVENT_SIGNATURE)

> Description: function returns wallet by signature

  ```
  # 'signature' = signature of the type of transaction that will be searched for
  ```

- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import SushiSwap

  f12 = SushiSwap.get_wallet_by_tx('0x397FF1542f962076d0BFE58eA045FfA2d347ACa0', 'latest', ETHEREUM)

  print(f12)

  ```

  ```
  output: None
  ```
  </details>

### 13: get_rewards_per_unit(lptoken_address, blockchain, web3=None, block='latest')

> Description: function returns rewards per unit for given lp token

- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import SushiSwap

  f13 = SushiSwap.get_rewards_per_unit('0x397FF1542f962076d0BFE58eA045FfA2d347ACa0', ETHEREUM)

  print(f13)
  ```

  ```
  output: 
  [{'sushi_address': '0x6B3595068778DD592e39A122f4f5a5cF09C90fE2', 'sushiPerBlock': 7.81054736315921e+17}]
  ```
  </details>


### 14: update_db()

> Description: function updates the db
