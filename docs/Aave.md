# Aave

## Defined in Aave.py


### 1: get_reserves_tokens(pdp_contract, block)

> Description: function returns reserved tokens for aave protocol v2

- <details><summary><b>Example</b></summary>

  ```
  from defyes.functions import *

  from defyes import Aave

  f1 = get_contract('0x057835Ad21a177dbdd3090bB1CAE03EaCF78Fc6d', ETHEREUM)

  f2 = Aave.get_reserves_tokens(f1, 'latest')

  print(f2)

  ```

  ```
  output:
  ['0xdAC17F958D2ee523a2206206994597C13D831ec7', '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599', '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', '0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e', '0xE41d2489571d322189246DaFA5ebDe1F4699F498', '0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984', '0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9', '0x0D8775F648430679A709E98d2b0Cb6250d2887EF', '0x4Fabb145d64652a948d72533023f6E7A623C7C53', '0x6B175474E89094C44Da98b954EedeAC495271d0F', '0xF629cBd94d3791C9250152BD8dfBDF380E2a3B9c', '0xdd974D5C2e2928deA5F71b9825b8b646686BD200', '0x514910771AF9Ca656af840dff83E8264EcF986CA', '0x0F5D2fB29fb7d3CFeE444a200298f468908cC942', '0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2', '0x408e41876cCCDC0F92210600ef50372656052a38', '0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F', '0x57Ab1ec28D129707052df4dF418D58a2D46d5f51', '0x0000000000085d4780B73119b644AE5ecd22b376', '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', '0xD533a949740bb3306d119CC777fa900bA034cd52', '0x056Fd409E1d7A124BD7017459dFEa2F387b6d5Cd', '0xba100000625a3754423978a60c9317c58a424e3D', '0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272', '0xD5147bc8e386d91Cc5DBE72099DAC6C9b99276F5', '0x03ab458634910AaD20eF5f1C8ee96F1D6ac54919', '0xD46bA6D942050d489DBd938a2C909A5d5039A161', '0x8E870D67F660D95d5be530380D0eC0bd388289E1', '0x1494CA1F11D487c2bBe4543E90080AeBa4BA3C2b', '0x853d955aCEf822Db058eb8505911ED77F175b99e', '0x956F47F50A910163D8BF957Cf5846D573E7f87CA', '0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84', '0xC18360217D8F7Ab5e7c516566761Ea12Ce7F9D72', '0xa693B19d2931d498c5B318dF961919BB4aee87a5', '0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B', '0x111111111117dC0aa78b770fA6A738034120C302', '0x5f98805A4E8be255a32880FDeC7F6728C6568bA0']
  ```
  </details>

### 2: get_reserves_tokens_balances(web3, wallet, block, blockchain, decimals=True)

> Description: function returns reserved token ballances for given wallet

- <details><summary><b>Example</b></summary>

  ```
  from defyes.functions import *

  from defyes import Aave

  web3 = get_node(ETHEREUM, 'latest', 0)

  f2 = Aave.get_reserves_tokens_balances(web3, '0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', ETHEREUM)

  print(f2)

  ```

  ```
  output: [['0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599', -25.1759987], ['0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84', 1385.4727732126728]]
  
  ```
  </details>

### 3: get_data(wallet, block, blockchain, execution = 1, web3=None, index=0, decimals=True)

> Description: function returns aave protocol data for given wallet

- <details><summary><b>Example</b></summary>

  ```
  from defyes.functions import *

  from defyes import Aave

  f3 = Aave.get_data('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', ETHEREUM)

  print(f3)

  ```

  ```
  output: 

  {'collateral_ratio': 422.8517007532872, 'liquidation_ratio': 120.48192771084337, 'eth_price_usd': 1321.28, 'collaterals': [{'token_address': '0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84', 'token_amount': 1385.4727732126728, 'token_price_usd': 1309.82714496}], 'debts': [{'token_address': '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599', 'token_amount': 25.17600199, 'token_price_usd': 17046.574635530906}]}
  
  ```
  </details>


### 4: get_all_rewards(wallet, block, blockchain, execution = 1, web3=None, index=0, decimals=True)

> Description: function returns all the rewards for given wallet from aave protocol

- <details><summary><b>Example</b></summary>

  ```
  from defyes.functions import *

  from defyes import Aave

  f4 = Aave.get_all_rewards('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', ETHEREUM)

  print(f4)

  ```

  ```
  output: 

  [['0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9', 5.046433045046507]]
  
  ```

### 5: underlying(wallet, block, blockchain, execution=1, web3=None, index=0, decimals=True, reward=False)

> Description: function returns underlying tokens for given wallter from aave protocol

- <details><summary><b>Example</b></summary>

  ```
  from defyes.functions import *

  from defyes import Aave

  f5 = Aave.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', 'latest', ETHEREUM, reward=True)

  print(f5)

  ```

  ```
  output: 

  [[['0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599', -25.17600614], ['0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84', 1385.4727732126728]], [['0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9', 5.046433045046507]]]
  
  ```


