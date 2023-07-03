# Bancor

## Defined in Bancor.py

### 1: underlying(token_address, wallet, block, blockchain, web3=None, execution=1, index=0, decimals=True, reward=False)

> Description: function returns the underlying token from bancor protocol for given wallet

- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import Bancor

  f1 = Bancor.underlying('0x36FAbE4cAeF8c190550b6f93c306A5644E7dCef6', '0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', ETHEREUM)

  print(f1)

  ```

  ```
  output: 
  [['0x903bEF1736CDdf2A537176cf3C64579C3867A881', 41633.599736141], ['0x1F573D6Fb3F13d689FF844B4cE37794d79a7FF1C', 0.0]]
  ```
  </details>


### 2: underlying_all(wallet, block, blockchain, web3=None, execution=1, index=0, decimals=True, reward=False)

> Description: function returns all underlying tokens for given wallet

- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import Bancor

  f2 = Bancor.underlying_all('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', ETHEREUM)

  print(f2)
  ```

  ```
  output: None
  ```
  </details>


