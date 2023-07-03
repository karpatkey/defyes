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

  web3 = get_node(ETHEREUM, 'latest', 0)
  f1 = Curve.get_registry_contract(web3, 3, 'latest', ETHEREUM)
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

  web3 = get_node(XDAI, 'latest', 0)
  
  web3 = get_node(XDAI, 'latest', 0)
  
  f2 = Curve.get_pool_gauge_address(web3, '0x7f90122BF0700F9E7e1F688fe926940E8839F353', '0x1337BedC9D22ecbe766dF105c9623922A27963EC', 'latest', XDAI)

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

  f3 = Curve.get_gauge_version('0x1891E46859DBf78EeEfb652425755494eE8aD7bf', 'latest', XDAI)

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

  web3 = get_node(XDAI, 'latest', 0)
  
  f4 = Curve.get_pool_address(web3, '0x1337BedC9D22ecbe766dF105c9623922A27963EC', 'latest', XDAI)
  
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

  web3 = get_node(ETHEREUM, 'latest', 0)
  
  f5 = Curve.get_pool_data(web3, '0xD51a44d3FaE010294C616388b506AcdA1bfAAE46', 'latest', ETHEREUM)

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

  f6 = Curve.get_lptoken_data('0xc4AD29ba4B3c580e6D59105FFf484999997675Ff', 'latest', ETHEREUM)

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

  f7 = Curve.get_all_rewards('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0xc4AD29ba4B3c580e6D59105FFf484999997675Ff', 'latest', ETHEREUM)

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

  f8 = Curve.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0x1337BedC9D22ecbe766dF105c9623922A27963EC', 'latest', XDAI )

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

  f10 = Curve.pool_balances('0x1337BedC9D22ecbe766dF105c9623922A27963EC', 'latest', XDAI)

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

  f11 = Curve.swap_fees('0x1337BedC9D22ecbe766dF105c9623922A27963EC', 25913602, 'latest', XDAI)

  print(f11)

  
  ```

  ```
  output: 
  {'swaps': [{'block': 25913682, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.0019992133127874276}, {'block': 25913701, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.007333559800511542}, {'block': 25913721, 'tokenOut': '0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83', 'amountOut': 0.6397394164}, {'block': 25913783, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.0008607565751133651}, {'block': 25913910, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.037022720405197725}, {'block': 25913948, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.039984303471116825}, {'block': 25913970, 'tokenOut': '0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83', 'amountOut': 0.4002363776}, {'block': 25914114, 'tokenOut': '0x4ECaBa5870353805a9F068101A40E0f32ed605C6', 'amountOut': 0.007996171600000001}, {'block': 25914144, 'tokenOut': '0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83', 'amountOut': 0.0066172976}, {'block': 25914200, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.0014729267096921916}, {'block': 25914330, 'tokenOut': '0x4ECaBa5870353805a9F068101A40E0f32ed605C6', 'amountOut': 0.0039983932}, {'block': 25914416, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.008602286827199044}, {'block': 25914750, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.022511488698351036}, {'block': 25914759, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.006614704715056072}, {'block': 25914759, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.6997249291194675}, {'block': 25915143, 'tokenOut': '0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83', 'amountOut': 0.13503600880000002}, {'block': 25915224, 'tokenOut': '0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83', 'amountOut': 0.11770507120000001}, {'block': 25915235, 'tokenOut': '0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83', 'amountOut': 0.117932982}, {'block': 25915309, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.021514701714473644}, {'block': 25915340, 'tokenOut': '0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83', 'amountOut': 0.005720752000000001}, {'block': 25915455, 'tokenOut': '0x4ECaBa5870353805a9F068101A40E0f32ed605C6', 'amountOut': 1.499395634}, {'block': 25915655, 'tokenOut': '0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83', 'amountOut': 0.05997549320000001}, {'block': 25915684, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.00030144913310451685}, {'block': 25915782, 'tokenOut': '0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83', 'amountOut': 0.0219822164}, {'block': 25915803, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.02242247669985942}, {'block': 25915834, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.0004494915495654226}, {'block': 25915864, 'tokenOut': '0x4ECaBa5870353805a9F068101A40E0f32ed605C6', 'amountOut': 0.0843659144}, {'block': 25915973, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.02079185759339624}, {'block': 25916016, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.09113021136366664}, {'block': 25916018, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.001970104549943838}, {'block': 25916024, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.0011432944757581813}, {'block': 25916028, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.0014962398019174262}, {'block': 25916156, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.2998824374160615}, {'block': 25916435, 'tokenOut': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 'amountOut': 0.0006173702201516521}]}
  
  ```
  </details>

