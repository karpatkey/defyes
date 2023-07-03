# Elk

## Defined in Elk.py

### 1: get_lptoken_data(lptoken_address, block, blockchain, web3=None, execution=1, index=0)

> Description: function returns lp token data on ELK protocol

- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import Elk


  f1 = Elk.get_lptoken_data('0xA27E5775317F3f301B5b08BabCdE0a20FEAE7f09', 'latest', ETHEREUM)

  print(f1)

  ```

  ```
  output:
  {'contract': <web3._utils.datatypes.Contract object at 0x7fb03eef26b0>, 'decimals': 18, 'totalSupply': 3079557346471436960125, 'token0': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'token1': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'reserves': [29056721408238148310, 347561671694311785474636, 1673509307], 'kLast': 0, 'virtualTotalSupply': 3079557346471436960125}
  
  ```
  </details>


### 2: get_pool_address(web3, token0, token1, block, blockchain)

> Description: function returns pool addres based on given token pair on Elk protocol


- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import Elk

  web3 = get_node(ETHEREUM, 'latest', 0)
  
  f2 = Elk.get_pool_address(web3, '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'latest', ETHEREUM)
  
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

  web3 = get_node(ETHEREUM, 'latest', 0)
  f2 = get_contract('0xF220eA963D27Ebe782f09403017B29692A4fC4aE', ETHEREUM)
  f3 = Elk.get_elk_rewards(web3, f2, '0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', ETHEREUM)

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

  web3 = get_node(ETHEREUM, 'latest', 0)
  f3 = get_contract('0xF220eA963D27Ebe782f09403017B29692A4fC4aE', ETHEREUM)
  f4 = Elk.get_booster_rewards(web3, f3, '0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', ETHEREUM)
  
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

  f5 = Elk.get_all_rewards('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0xF220eA963D27Ebe782f09403017B29692A4fC4aE', 'latest', ETHEREUM)

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

  f6 = Elk.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0xA27E5775317F3f301B5b08BabCdE0a20FEAE7f09', 'latest', ETHEREUM)

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

  f7 = Elk.pool_balances('0xA27E5775317F3f301B5b08BabCdE0a20FEAE7f09', 'latest', ETHEREUM)
  
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

  f8 = Elk.swap_fees('0xA27E5775317F3f301B5b08BabCdE0a20FEAE7f09', 16380015, 'latest', ETHEREUM)

  print(f8)

  ```

  ```
  output: 
  {'swaps': [{'block': 16381797, 'token': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'amount': 2.889438460326057}, {'block': 16382996, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 3e-09}, {'block': 16385571, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 0.00255}, {'block': 16385667, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 0.0009}, {'block': 16385691, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 9e-06}, {'block': 16385812, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 0.00015}, {'block': 16385831, 'token': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'amount': 26.723058285543605}, {'block': 16385839, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 0.00017571833246287513}, {'block': 16385938, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 6e-05}, {'block': 16385957, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 3.6e-05}, {'block': 16385975, 'token': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'amount': 12.83912818935761}, {'block': 16386009, 'token': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'amount': 0.39853215112316875}, {'block': 16386450, 'token': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'amount': 31.327314122523138}, {'block': 16386451, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 0.0014496276567174053}, {'block': 16386524, 'token': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'amount': 36.478903268343565}, {'block': 16386527, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 0.0018}, {'block': 16386537, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 0.0005028085391423697}, {'block': 16386559, 'token': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'amount': 23.07109673165644}, {'block': 16386561, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 0.0015010243909154}, {'block': 16387375, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 1.2028675361808711e-05}, {'block': 16387414, 'token': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'amount': 2.957184093901322}, {'block': 16388603, 'token': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'amount': 7.1615954570745695}, {'block': 16388771, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 1.5e-05}, {'block': 16388955, 'token': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'amount': 6.3083888292692265}, {'block': 16388990, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 0.0007353592629198234}, {'block': 16389072, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 0.00021921}, {'block': 16389072, 'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amount': 0.00255}, {'block': 16389072, 'token': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'amount': 2.65335036}, {'block': 16389108, 'token': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'amount': 9.0}, {'block': 16389299, 'token': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE', 'amount': 11.890786090090941}]}
   
  ```
  </details>


