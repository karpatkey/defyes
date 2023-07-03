# Maker

## Defined in Maker.py

### 1: get_vault_data(vault_id, block, web3=None, execution=1, index=0)

> Description: function returns valut data for given valut id

- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import Maker

  f1 = Maker.get_vault_data(1, 'latest')
  
  print(f1)

  ```

  ```
  output:
  {'mat': 1.45, 'gem': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'dai': '0x6B175474E89094C44Da98b954EedeAC495271d0F', 'ink': 0.0, 'art': 0.0, 'Art': 193027523.3855285, 'rate': 1.0835304604763405, 'spot': 963.8172413793103, 'line': 368907736.31731033, 'dust': 15000.0}
  
  ```
  </details>


### 2: underlying(vault_id, block, web3=None, execution=1, index=0)

> Description: function returns underlying tokens for given wallet for given vault id on maker protocol

  ```
  # Output:
  # 1 - Tuple: [[collateral_address, collateral_amount], [debt_address, -debt_amount]]
  ```
- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import Maker

  f2 = Maker.underlying(1, 'latest')
  
  print(f2)

  ```

  ```
  output:
  [['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 0.0], ['0x6B175474E89094C44Da98b954EedeAC495271d0F', -0.0]]
  
  
  ```
  </details>
