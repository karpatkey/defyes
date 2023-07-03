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

  web3 = get_node(ETHEREUM, 'latest', 0)
  f1 = get_contract('0xf34DFF761145FF0B05e917811d488B441F33a968', ETHEREUM)
  f2 = Convex.get_rewards(web3, f1, '0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', ETHEREUM)
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

  web3 = get_node(ETHEREUM, 'latest', 0)
  f1 = get_contract('0xf34DFF761145FF0B05e917811d488B441F33a968', ETHEREUM)
  f3 = Convex.get_extra_rewards(web3, f1, '0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', ETHEREUM)
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

  f1 = get_contract('0xf34DFF761145FF0B05e917811d488B441F33a968', ETHEREUM)
  f4 = Convex.get_all_rewards('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'f1', 'latest', ETHEREUM)
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

  f5 = Convex.get_locked('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', ETHEREUM)
  
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

  f6 = Convex.get_staked('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', ETHEREUM)
  
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

  f7 = Convex.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0x9fC689CCaDa600B6DF723D9E47D84d76664a1F23', 'latest', ETHEREUM)
  
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

  f8 = Convex.pool_balances('0x9fC689CCaDa600B6DF723D9E47D84d76664a1F23', 'latest', ETHEREUM)
  
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
