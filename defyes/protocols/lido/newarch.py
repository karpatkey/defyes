"""
Ethereum: wstETH -> stETH -> ETH
Gnosis: wstETH -> stETH
"""
from defabipedia import Chain
from defabipedia.tokens import EthereumTokenAddr, GnosisTokenAddr

from defyes.portfolio import (
    DeployedToken,
    FrozenKwInit,
    NativeToken,
    TokenPosition,
    UnderlyingTokenPosition,
    Unwrappable,
)

from . import contracts


class LidoToken(DeployedToken):
    protocol = "lido"


ETH = NativeToken.objs.get(chain=Chain.ETHEREUM)


class StEthToken(LidoToken):
    contract_class = contracts.Steth
    symbol = "stETH"


class EthereumStEthToken(Unwrappable, StEthToken):
    chain = Chain.ETHEREUM

    def unwrap(self, token_position: TokenPosition) -> list[UnderlyingTokenPosition]:
        return [UnderlyingTokenPosition(token=ETH, amount_teu=token_position.amount_teu)]


eth_stETH = EthereumStEthToken(address=EthereumTokenAddr.stETH)
gnosis_stETH = StEthToken(chain=Chain.GNOSIS, address="0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84")


class WrappedStEthToken(Unwrappable, LidoToken):
    contract_class = contracts.Wsteth
    symbol = "wstETH"

    def unwrap(self, token_position: TokenPosition) -> list[UnderlyingTokenPosition]:
        self.contract.block = token_position.block  # TODO: improve this workarround
        amount_teu = token_position.amount * self.contract.st_eth_per_token
        return [UnderlyingTokenPosition(token=self.unwrapped_token, amount_teu=amount_teu)]


WrappedStEthToken.objs.create(chain=Chain.ETHEREUM, address=EthereumTokenAddr.wstETH, unwrapped_token=eth_stETH)
WrappedStEthToken.objs.create(chain=Chain.GNOSIS, address=GnosisTokenAddr.wstETH, unwrapped_token=gnosis_stETH)


class Positions(FrozenKwInit, list):
    pass


# patch decimals, because the unstETH contract has not decimals funcion.
LidoToken(chain=Chain.ETHEREUM, address=EthereumTokenAddr.unstETH, decimals=0)
