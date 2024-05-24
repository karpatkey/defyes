"""
Ethereum: wstETH -> stETH -> ETH
Gnosis: wstETH -> stETH
"""
from defabipedia import Chain
from defabipedia.tokens import EthereumTokenAddr, GnosisTokenAddr

from defyes.portfolio import DeployedToken, Frozen, KwInit, NativeToken, TokenAmount, UnderlyingTokenAmount, Unwrappable

from . import contracts


class LidoToken(DeployedToken):
    protocol = "lido"


ETH = NativeToken.objs.get(chain=Chain.ETHEREUM)


class StEthToken(LidoToken):
    contract_class = contracts.Steth
    symbol = "stETH"


class EthereumStEthToken(Unwrappable, StEthToken):
    chain = Chain.ETHEREUM

    def unwrap(self, tokenamount: TokenAmount) -> list[UnderlyingTokenAmount]:
        self.abi.block = tokenamount.block  # TODO: improve this workarround
        return [UnderlyingTokenAmount(token=ETH, amount_teu=tokenamount.amount_teu)]


eth_stETH = EthereumStEthToken(address=EthereumTokenAddr.stETH)
gnosis_stETH = StEthToken(chain=Chain.GNOSIS, address="0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84")


class WrappedStEthToken(Unwrappable, LidoToken):
    contract_class = contracts.Wsteth
    symbol = "wstETH"

    def unwrap(self, tokenamount: TokenAmount) -> list[UnderlyingTokenAmount]:
        self.abi.block = tokenamount.block  # TODO: improve this workarround
        amount_teu = tokenamount.amount * self.abi.st_eth_per_token
        return [UnderlyingTokenAmount(token=self.unwrapped_token, amount_teu=amount_teu)]


WrappedStEthToken(chain=Chain.ETHEREUM, address=EthereumTokenAddr.wstETH, unwrapped_token=eth_stETH)
WrappedStEthToken(chain=Chain.GNOSIS, address=GnosisTokenAddr.wstETH, unwrapped_token=gnosis_stETH)


class Positions(Frozen, KwInit, list):
    pass


# patch decimals, because the unstETH contract has not decimals funcion.
LidoToken(chain=Chain.ETHEREUM, address=EthereumTokenAddr.unstETH, decimals=0)
