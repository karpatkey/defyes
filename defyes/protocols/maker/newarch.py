import logging
from typing import Iterator

from defabipedia import Blockchain, Chain
from defabipedia.tokens import EthereumTokenAddr

from defyes.portfolio import (
    DeployedToken,
    FrozenKwInit,
    NativeToken,
    Position,
    Token,
    TokenPosition,
    UnderlyingTokenPosition,
    Unwrappable,
    default,
    repr_for,
)

from . import contracts

logger = logging.getLogger(__name__)

xDAI = NativeToken.objs.get(chain=Chain.GNOSIS)


class MakerToken(DeployedToken):
    protocol = "maker"


MakerToken(symbol="MKR", chain=Chain.ETHEREUM, address=EthereumTokenAddr.MKR)
eth_DAI = MakerToken(symbol="DAI", chain=Chain.ETHEREUM, address=EthereumTokenAddr.DAI)


class SdaiToken(Unwrappable, MakerToken):
    contract_class = contracts.Sdai
    unwrapped_token: Token

    def unwrap(self, token_position: TokenPosition) -> list[UnderlyingTokenPosition]:
        self.contract.block = token_position.block  # TODO: improve this workarround
        amount_teu = self.contract.convert_to_assets(token_position.amount_teu)
        return [UnderlyingTokenPosition(token=self.unwrapped_token, amount_teu=amount_teu)]


SdaiToken(
    symbol="sDAI", chain=Chain.ETHEREUM, address="0x83F20F44975D03b1b09e64809B757c47f942BEeA", unwrapped_token=eth_DAI
)
SdaiToken(symbol="sDAI", chain=Chain.GNOSIS, address="0xaf204776c7245bF4147c2612BF6e5972Ee483701", unwrapped_token=xDAI)


class MakerPosition(Position):
    protocol: str = "maker"
    context: "Positions"
    address: str


class Vault(MakerPosition):
    id: int
    __repr__ = repr_for("address", "id", "underlying", "unclaimed_rewards")


# WIP
class CDPManagerPosition(MakerPosition):
    def vault_ids(self, proxy_addr: str) -> list[int]:
        # next_id = self.contract.functions.first(proxy_addr).call(block_identifier=self.block)
        next_id = self.first(proxy_addr)
        for _ in range(self.count(proxy_addr)):
            yield next_id
            prev_id, next_id = self._list(next_id)


class DSR(MakerPosition):
    name = "manager"


class DSRPot(MakerPosition):
    name = "dsr_pot"


class Iou(MakerPosition):
    pass


class Positions(FrozenKwInit):
    wallet: str
    chain: Blockchain
    block: int

    __repr__ = repr_for("wallet", "chain", "block")

    def __iter__(self) -> Iterator[Position]:
        yield from self.vaults
        if self.dsr:
            yield self.dsr
        if self.dsr_pot:
            yield self.dsr_pot
        if self.iou:
            yield self.iou

    @default
    def DAI(self):
        return DeployedToken.objs.get(chain=self.chain, symbol="DAI")

    @default
    def vaults(self) -> list[Vault]:
        # contracts = defabipedia.maker.ContractSpecs[self.chain]
        # node = get_node(self.chain)
        # cdp = contracts.CdpManager.contract(node)
        cdp = contracts.CdpManager(self.chain, self.block)
        ilk_registry = contracts.IlkRegistry(self.chain, self.block)
        vat = contracts.Vat(self.chain, self.block)
        for vault_id in cdp.get_vault_ids(contracts.ProxyRegistry(self.chain, self.block).proxies(self.wallet)):
            ilk = cdp.ilks(vault_id)
            gem = ilk_registry.info(ilk)[4]
            urn_handler_address = cdp.urns(vault_id)
            ink, art = vat.urns(ilk, urn_handler_address)
            rate = vat.ilks(ilk)[1]

            lend_token = DeployedToken.objs.get_or_create(chain=self.chain, address=gem)
            yield Vault(
                address=cdp.contract.address,
                id=vault_id,
                context=self,
                underlying=[
                    UnderlyingTokenPosition(token=lend_token, amount_teu=ink, block=self.block),
                    UnderlyingTokenPosition(token=self.DAI, amount_teu=-1 * art * rate, block=self.block),
                ],
                rate=rate,
            )

    @default
    def dsr(self) -> DSR:
        dsr = contracts.DsrManager(self.chain, self.block)
        return DSR(
            context=self,
            address=dsr.contract.address,
            underlying=[UnderlyingTokenPosition(token=self.DAI, amount_teu=dsr.dai_balance(self.wallet))],
        )

    @default
    def dsr_pot(self) -> DSRPot:
        pot = contracts.Pot(self.chain, self.block)
        return DSRPot(
            context=self,
            address=pot.contract.address,
            underlying=[UnderlyingTokenPosition(token=self.DAI, amount_teu=pot.pie_1(self.wallet) * pot.chi_decimal)],
        )

    @default
    def iou(self) -> Iou:
        iou = contracts.Iou(self.chain, self.block)
        MKR = DeployedToken.objs.get(chain=self.chain, symbol="MKR")
        return Iou(
            context=self,
            address=iou.contract.address,
            underlying=[UnderlyingTokenPosition(token=MKR, amount_teu=iou.balance_of(self.wallet))],
        )
