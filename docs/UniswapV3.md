# UniswapV3

## Defined in UniswapV3.py


### 1: get_rate_uniswap_v3(token_src, token_dst, block, blockchain, web3=None, execution=1, index=0, fee=100)

> Description: function returns 

*** Help Needed ***

- <details><summary><b>Example</b></summary>

  ```
 

  ```

  ```
  output: 
  
  
  ```
  </details>


### 2: underlying(wallet, nftid, block, blockchain, web3=None, execution=1, index=0, decimals=True)

> Description: function returns underlying tokens for given wallter and nft id

- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import UniswapV3

  f2 = UniswapV3.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', 214704, 'latest', ETHEREUM)

  print(f2)

  ```

  ```
  output: 
  [['0x6810e776880C02933D47DB1b9fc05908e5386b96', 0], ['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 0]]
  
  
  ```
  </details>

### 3: allnfts(wallet, block, blockchain, web3=None, execution=1, index=0)

> Description: function returns all nfts for given wallet on UniswapV3 protocol

- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import UniswapV3

  f3 = UniswapV3.allnfts('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', ETHEREUM)

  print(f3)

  ```

  ```
  output: [185085, 186529, 189493, 214704, 214707, 214716, 218573, 220361, 217714, 286920, 339884, 346143, 358770]
  
  
  ```
  </details>


### 3: get_fee(nftid, block, blockchain, web3=None, execution=1, index=0, decimals=True)

> Description: function returns fees for given nft id on UniswapV3 protocol


- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import UniswapV3

  f4 = UniswapV3.get_fee(346143, 'latest', ETHEREUM)

  print(f4)

  ```

  ```
  output: 
  [['0x6810e776880C02933D47DB1b9fc05908e5386b96', 0.0], ['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 0.0]]
  
  
  ```
  </details>
