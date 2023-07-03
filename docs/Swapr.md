# Swapr

## Defined in Swapr.py

### 1: get_staking_rewards_contract(web3, block, blockchain)

> Description: function returns stacking rewards contract


- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import Swapr

  web3 = get_node(ETHEREUM, 'latest', 0)

  f1 = Swapr.get_staking_rewards_contract(web3, 'latest', ETHEREUM)

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

  web3 = get_node(ETHEREUM, 'latest', 0)

  f1 = Swapr.get_staking_rewards_contract(web3, 'latest', ETHEREUM)

  f2 = Swapr.get_distribution_contracts(web3, '0x7515Be43D16f871588ADc135d58a9c30A71Eb34F', f1, 1, 'latest', ETHEREUM)

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

  f3 = Swapr.get_lptoken_data('0x7515Be43D16f871588ADc135d58a9c30A71Eb34F', 'latest', ETHEREUM)

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

  f4 = Swapr.get_all_rewards('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0x7515Be43D16f871588ADc135d58a9c30A71Eb34F', 'latest', ETHEREUM)

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

  f5 = Swapr.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0x7515Be43D16f871588ADc135d58a9c30A71Eb34F', 'latest', ETHEREUM)

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

  f6 = Swapr.pool_balances('0x7515Be43D16f871588ADc135d58a9c30A71Eb34F', 'latest', ETHEREUM)

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

  f7 = Swapr.swap_fees('0x7515Be43D16f871588ADc135d58a9c30A71Eb34F', 16392504, 'latest', ETHEREUM)

  print(f7)

  ```

  ```
  output: 
  {'swaps': [{'block': 16392554, 'token': '0x6B175474E89094C44Da98b954EedeAC495271d0F', 'amount': 0.3533967616636148}, {'block': 16392693, 'token': '0x6B175474E89094C44Da98b954EedeAC495271d0F', 'amount': 0.8042712308268711}, {'block': 16392942, 'token': '0x6B175474E89094C44Da98b954EedeAC495271d0F', 'amount': 1.3125}, {'block': 16392986, 'token': '0x6B175474E89094C44Da98b954EedeAC495271d0F', 'amount': 1.12284669760275}, {'block': 16393054, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 4.3810185944715885e-05}, {'block': 16393185, 'token': '0x6B175474E89094C44Da98b954EedeAC495271d0F', 'amount': 0.13697197835428987}, {'block': 16393190, 'token': '0x6B175474E89094C44Da98b954EedeAC495271d0F', 'amount': 0.1027289837657174}, {'block': 16393338, 'token': '0x6B175474E89094C44Da98b954EedeAC495271d0F', 'amount': 0.2434762712795}, {'block': 16393463, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 0.00035039806149557873}, {'block': 16393467, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 0.000173850319209059}]}
  
  ```
  </details>

