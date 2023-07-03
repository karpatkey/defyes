# Unit

## Defined in Unit.py


### 1: get_vault_address(blockchain)

> Description: function returns vault address for given blockchain

- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import Unit

  f1 = Unit.get_vault_address(ETHEREUM)

  print(f1)

  ```

  ```
  output: 0xb1cFF81b9305166ff1EFc49A129ad2AfCd7BCf19
  

  ```
  </details>


### 2: get_cdp_registry_address(blockchain)

> Description: function returns cdp registry address for given blockchain

- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import Unit

  f2 = Unit.get_cdp_registry_address(ETHEREUM)

  print(f2)

  ```

  ```
  output: 0x1a5Ff58BC3246Eb233fEA20D32b79B5F01eC650c
  

  ```
  </details>

### 3: get_cdp_manager_address(blockchain)

> Description: function returns cdp manager for given blockchain

- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import Unit

  f3 = Unit.get_cdp_manager_address(ETHEREUM)

  print(f3)

  ```

  ```
  output: 0x69FB4D4e3404Ea023F940bbC547851681e893a91

  ```
  </details>


### 4: get_cdp_viewer_address(blockchain)

> Description: function retunrs cdp viewer address for given blockchain


- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import Unit

  f4 = Unit.get_cdp_viewer_address(ETHEREUM)

  print(f4)

  ```

  ```
  output: 0x68AF7bD6F3e2fb480b251cb1b508bbb406E8e21D
  
  ```
  </details>

### 5: get_cdp_viewer_data(wallet, collateral_address, block, blockchain, web3=None, execution=1, index=0, decimals=True)

> Description: function returns cdp viewer data for given wallet and collateral address

- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import Unit

  f5 = Unit.get_cdp_viewer_data('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'latest', ETHEREUM)

  print(f5)

  ```

  ```
  output: {}
  
  ```
  </details>

### 6: get_cdp_data(wallet, collateral_address, block, blockchain, web3=None, execution=1, index=0, decimals=True)

> Description: function returns cdp data for given wallet and collateral address


- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import Unit

  f6 = Unit.get_cdp_data('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'latest', ETHEREUM)

  print(f6)

  ```

  ```
  output: {}
  
  ```
  </details>


### 7: underlying(wallet, block, blockchain, web3=None, execution=1, index=0, decimals=True)

> Description: function returns underlying tokens for given wallet on Unit protocol

  ```
  # Output: a list with N elements, where N = number of CDPs for the wallet:
  # 1 - List of Tuples: [[collateral_addressN, collateral_amountN], [debt_addressN, -debt_amountN]]
  
  ```
- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import Unit

  f7 = Unit.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', ETHEREUM)

  print(f7)

  ```

  ```
  output: []
  
  ```
  </details>
