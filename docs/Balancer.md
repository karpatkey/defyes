# Balancer

## Defined in Balancer.py

### 1: get_lptoken_data(lptoken_address, block, blockchain, web3=None, execution=1, index=0)

> Description: function returns lp token data from balancer protocol

- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import Balancer

  f1 = Balancer.get_lptoken_data('0x7B50775383d3D6f0215A8F290f2C9e2eEBBEceb2', 'latest', ETHEREUM)

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

  
  web3 = get_node(ETHEREUM, 'latest', 0)
  f1 = get_contract('0x68d019f64A7aa97e2D4e7363AEE42251D08124Fb', ETHEREUM)

  f2 = Balancer.get_bal_rewards(web3, 'f1', '0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', ETHEREUM)

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

  web3 = get_node(ETHEREUM, 'latest', 0)
  f1 = get_contract('0x68d019f64A7aa97e2D4e7363AEE42251D08124Fb', ETHEREUM)
  f3 = Balancer.get_rewards(web3, f1, '0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', ETHEREUM, decimals=True)
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

  web3 = get_node(ETHEREUM, 'latest', 0)
  f4 = Balancer.get_vebal_rewards(web3, '0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', ETHEREUM, decimals=True)
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
  
  f5 = Balancer.get_all_rewards('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0x7B50775383d3D6f0215A8F290f2C9e2eEBBEceb2', 'latest', ETHEREUM)
  
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
  
  f6 = Balancer.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0x7B50775383d3D6f0215A8F290f2C9e2eEBBEceb2', 'latest', ETHEREUM)
  
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
  
  f7 = Balancer.pool_balances('0x7B50775383d3D6f0215A8F290f2C9e2eEBBEceb2', 'latest', ETHEREUM) 

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
  
  f8 = Balancer.swap_fees('0x7B50775383d3D6f0215A8F290f2C9e2eEBBEceb2', 16374265, 'latest', ETHEREUM)

  print(f8)

  ```

  ```
  output: 
  {'swaps': [{'block': 16376941, 'tokenIn': '0x9210F1204b5a24742Eba12f710636D76240dF3d0', 'amountIn': 0.8095032036253991}, {'block': 16378850, 'tokenIn': '0x804CdB9116a10bB78768D3252355a1b18067bF8f', 'amountIn': 0.9885184780730925}]}
  
  ```
  </details>
