# QiDao

## Defined in QiDao.py

### 1: get_vault_address(collateral_address, blockchain)

> Description: function returns vault address based on given collateral address

- <details><summary><b>Example</b></summary>

  ```
  
  from defyes import *

  from defyes.functions import *

  from defyes import QiDao

  f1 = QiDao.get_vault_address('0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb', XDAI)

  print(f1)

  ```

  ```
  output: 0x014A177E9642d1b4E970418f894985dC1b85657f
  
  ```
  </details>

### 2: get_vault_data(vault_id, collateral_address, block, blockchain, web3=None, execution=1, index=0, decimals=True)

> Description: function returns vault data based on given vault id and collateral address


- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import QiDao

  f2 = QiDao.get_vault_data(1, '0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb', 'latest', XDAI)

  print(f2)


  ```

  ```
  output: 
  {'collateral_address': '0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb', 'collateral_amount': 0.0, 'collateral_token_usd_value': 96.15, 'debt_address': '0x3F56e0c36d275367b8C502090EDF38289b3dEa0d', 'debt_amount': 0.0, 'debt_token_usd_value': 0.9920834072195736, 'debt_usd_value': 0, 'collateral_ratio': None, 'available_debt_amount': 203205.79297252028, 'liquidation_ratio': 130, 'liquidation_price': None}
  
  ```
  </details>

### 3: underlying(vault_id, collateral_address, block, blockchain, web3=None, execution=1, index=0, decimals=True)

> Description: function returns underlying tokens for given vault id and collateral address

  ```
  # Output:
  # 1 - Tuple: [[collateral_address, collateral_amount], [debt_address, -debt_amount]]
  ```

- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import QiDao

  f3 = QiDao.underlying(1, '0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb', 'latest', XDAI)

  print(f3)

  ```

  ```
  output: 
  [['0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb', 0.0], ['0x3F56e0c36d275367b8C502090EDF38289b3dEa0d', 0.0]]
  
  ```
  </details>
