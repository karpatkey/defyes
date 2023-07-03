# Reflexer

## Defined in Reflexer.py

### 1: lptoken_underlying(lptoken_address, amount, block, blockchain)

> Description: fucntion returns underlying tokens for given lp token on Reflexer protocol

- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import Reflexer

  f1 = Reflexer.lptoken_underlying('0xd6F3768E62Ef92a9798E5A8cEdD2b78907cEceF9', 10000, 'latest', ETHEREUM)

  print(f1)


  ```

  ```
  output:
  [['0x6243d8cea23066d098a15582d81a598b4e8391f4', 51479.35989733311], ['0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 524.5602730745637]]
  [['0x6243d8cea23066d098a15582d81a598b4e8391f4', 51479.35989733311], ['0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 524.5602730745637]]
  [['0x6243d8cea23066d098a15582d81a598b4e8391f4', 115095.22732025111], ['0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 1172.7881619564894]]
  ```
  </details>


### 2: pool_balance(lptoken_address, block, blockchain)

> Description: fucntion returns pool balance for given lp token

- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import Reflexer

  f2 = Reflexer.pool_balance('0xd6F3768E62Ef92a9798E5A8cEdD2b78907cEceF9', 'latest', ETHEREUM)

  print(f2)

  ```

  ```
  output:
  [['0x6243d8cea23066d098a15582d81a598b4e8391f4', 51479.35989733311], ['0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 524.5602730745637]]
  [['0x6243d8cea23066d098a15582d81a598b4e8391f4', 51479.35989733311], ['0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 524.5602730745637]]
  [['0x6243d8cea23066d098a15582d81a598b4e8391f4', 129190.50613850323], ['0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 1316.4151091584395]]
  
  ```
  </details>

### 3: balance_of_lptoken_underlying(address, lptoken_address, block, blockchain)

> Description: fucntion returns balance of underlying tokens for given lp token

- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import Reflexer

  f3 = Reflexer.balance_of_lptoken_underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0xd6F3768E62Ef92a9798E5A8cEdD2b78907cEceF9', 'latest', ETHEREUM)

  print(f3)
  ```

  ```
  output:
  [['0x6243d8cea23066d098a15582d81a598b4e8391f4', 0.0], ['0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 0.0]]
  
  ```
  </details>


### 4: underlying(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0)

> Description: funstion returns underlying tokens for given wallet and lp token on Reflexer protocol

- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import Reflexer

  
  f4 = Reflexer.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0xd6F3768E62Ef92a9798E5A8cEdD2b78907cEceF9', 'latest', ETHEREUM)

  print(f4)
  ```

  ```
  output:
  [['0x6243d8cea23066d098a15582d81a598b4e8391f4', 51479.35989733311], ['0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 524.5602730745637]]
  
  ```
  </details>

