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

  f0 = get_contract('0xA57b8d98dAE62B26Ec3bcC4a365338157060B234', ETHEREUM)

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

  web3 = get_node(ETHEREUM, 'latest', 0)

  f1 = get_contract('0x00A7BA8Ae7bca0B10A32Ea1f8e2a1Da980c6CAd2', ETHEREUM)

  f2 = Aura.get_rewards(web3, f1, '0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', ETHEREUM)

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

  web3 = get_node(ETHEREUM, 'latest', 0)

  f1 = get_contract('0x00A7BA8Ae7bca0B10A32Ea1f8e2a1Da980c6CAd2', ETHEREUM)

  f3 = Aura.get_extra_rewards(web3, f1, '0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', ETHEREUM)

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

  f4 = Aura.get_extra_rewards_airdrop('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', ETHEREUM)

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

  f6 = Aura.get_all_rewards('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0xCfCA23cA9CA720B6E98E3Eb9B6aa0fFC4a5C08B9', 'latest', ETHEREUM)

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

  f7 = Aura.get_locked('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', ETHEREUM)

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

  f8 = Aura.get_staked('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', ETHEREUM)

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

  f9 = Aura.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0xCfCA23cA9CA720B6E98E3Eb9B6aa0fFC4a5C08B9', 'latest', ETHEREUM)

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

  f10 = Aura.pool_balances('0xCfCA23cA9CA720B6E98E3Eb9B6aa0fFC4a5C08B9', 'latest', ETHEREUM)

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
