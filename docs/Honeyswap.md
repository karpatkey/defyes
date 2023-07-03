# Honeyswap

## Defined in Honeyswap.py

### 1: get_lptoken_data(lptoken_address, block, blockchain, web3=None, execution=1, index=0)

> Description: function returns lp token data on Honeyswap protoocl


- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import Honeyswap

  f1 = Honeyswap.get_lptoken_data('0xCd9652F006EFDE64f07030F10A1945EAD8AC1855', 'latest', ETHEREUM)
  
  print(f1)

  ```

  ```
  output:
  {'contract': <web3._utils.datatypes.Contract object at 0x7fba31e8a710>, 'decimals': 18, 'totalSupply': 108503144715306467026, 'token0': '0x1957d368f6038F09faaE020d485b35718E0Eed1A', 'token1': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'reserves': [763270497078084747756, 15742597871023746342, 1607901903], 'kLast': 0, 'virtualTotalSupply': 1.3020377365836775e+20}  
  
  ```
  </details>


### 2: underlying(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True)

> Description: function returns underlying tokens for given wallet with given lptoken

  ```
  # Output: a list with 1 element:
  # 1 - List of Tuples: [liquidity_token_address, balance]
  ```

- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import Honeyswap

  f2 = Honeyswap.underlying('0x849D52316331967b6fF1198e5E32A0eB168D039d', '0xCd9652F006EFDE64f07030F10A1945EAD8AC1855', 'latest', ETHEREUM)

  print(f2)

  ```

  ```
  output:
  [['0x1957d368f6038F09faaE020d485b35718E0Eed1A', 0.0], ['0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 0.0]]

  ```
  </details>


### 3: pool_balances(lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True)

> Description: function returns pool balances for given lp token on Honeyswap protocol

  ```
  # Output: a list with 1 element:
  # 1 - List of Tuples: [liquidity_token_address, balance]
  ```

- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import Honeyswap

  f3 = Honeyswap.pool_balances('0xCd9652F006EFDE64f07030F10A1945EAD8AC1855', 'latest', ETHEREUM)

  print(f3)
  
  ```

  ```
  output:
  [['0x1957d368f6038F09faaE020d485b35718E0Eed1A', 763.2704970780848], ['0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 15.742597871023746]]

  ```
  </details>

### 4: swap_fees(lptoken_address, block_start, block_end, blockchain, web3=None, execution=1, index=0, decimals=True)

> Description: fucntion returns swap fees for given lp token for give reange of blocks

- <details><summary><b>Example</b></summary>

  ```
  from defyes import *

  from defyes.functions import *

  from defyes import Honeyswap

  f4 = Honeyswap.swap_fees('0xCd9652F006EFDE64f07030F10A1945EAD8AC1855', 0, 'latest', ETHEREUM)

  print(f4)

  ```

  ```
  output:
  {'swaps': [{'block': 11134367, 'token': '0x1957d368f6038F09faaE020d485b35718E0Eed1A', 'amount': 0.0005262109004007418}, {'block': 11134380, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.0038122294599445485}, {'block': 11134649, 'token': '0x1957d368f6038F09faaE020d485b35718E0Eed1A', 'amount': 0.000497428365687157}, {'block': 11134961, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.004008351883662104}, {'block': 11134984, 'token': '0x1957d368f6038F09faaE020d485b35718E0Eed1A', 'amount': 0.025735010568652947}, {'block': 11135972, 'token': '0x1957d368f6038F09faaE020d485b35718E0Eed1A', 'amount': 0.23927241967672228}, {'block': 11135972, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.001371294269959149}, {'block': 11136386, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.00149518324360386}, {'block': 11138426, 'token': '0x1957d368f6038F09faaE020d485b35718E0Eed1A', 'amount': 1.5}, {'block': 11138426, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.0005880163841135043}, {'block': 11141757, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.003}, {'block': 11143948, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.0009482496689891964}, {'block': 11153516, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.0009999}, {'block': 11153523, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.0015}, {'block': 11153530, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.0005001}, {'block': 11153581, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.0018}, {'block': 11168389, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.0020655702056233145}, {'block': 11210669, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.005054900815379415}, {'block': 11211315, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.005111990858317916}, {'block': 11211817, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.005679169733007941}, {'block': 11212191, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.0165}, {'block': 11212438, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.018518323978912336}, {'block': 11213214, 'token': '0x1957d368f6038F09faaE020d485b35718E0Eed1A', 'amount': 0.16961917796935855}, {'block': 11213827, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.023760662104344098}, {'block': 11216926, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.008840951952023836}, {'block': 11216935, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.010587407899320654}, {'block': 11216941, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.012907693813954431}, {'block': 11216952, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.016084013197213927}, {'block': 11216959, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.02059631880854048}, {'block': 11216965, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.02731565993218982}, {'block': 11216969, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.033512834207083994}, {'block': 11216969, 'token': '0x1957d368f6038F09faaE020d485b35718E0Eed1A', 'amount': 0.04565053353647096}, {'block': 11216973, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.03537631473540627}, {'block': 11218589, 'token': '0x1957d368f6038F09faaE020d485b35718E0Eed1A', 'amount': 0.02682485834232684}, {'block': 11229905, 'token': '0x1957d368f6038F09faaE020d485b35718E0Eed1A', 'amount': 0.05504515223226972}, {'block': 11240721, 'token': '0x1957d368f6038F09faaE020d485b35718E0Eed1A', 'amount': 0.16473663231733446}, {'block': 11243062, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.024}, {'block': 11246252, 'token': '0x1957d368f6038F09faaE020d485b35718E0Eed1A', 'amount': 0.3}, {'block': 11247278, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.015323293667631526}, {'block': 11428790, 'token': '0xC483ad6F9B80B38691E95b708DE1d46721366ce3', 'amount': 0.0011079232513274775}, {'block': 11447567, 'token': '0x1957d368f6038F09faaE020d485b35718E0Eed1A', 'amount': 1.5}]}
  

  ```
  </details>
