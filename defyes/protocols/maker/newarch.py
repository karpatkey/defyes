import logging
from typing import Iterator

from defabipedia import Blockchain, Chain
from defabipedia.tokens import EthereumTokenAddr

from defyes.portfolio import (
    ERC20Token,
    Frozen,
    KwInit,
    NativeToken,
    Position,
    TokenAmount,
    UnderlyingTokenAmount,
    Unwrappable,
    default,
    repr_for,
)

from . import contracts

logger = logging.getLogger(__name__)

xDAI = NativeToken.objs.get(chain=Chain.GNOSIS)


class MakerToken(ERC20Token):
    protocol = "maker"


MakerToken(symbol="MKR", chain=Chain.ETHEREUM, address=EthereumTokenAddr.MKR)
eth_DAI = MakerToken(symbol="DAI", chain=Chain.ETHEREUM, address=EthereumTokenAddr.DAI)


class SdaiToken(Unwrappable, MakerToken):
    abi_class = contracts.Sdai

    def unwrap(self, tokenamount: TokenAmount) -> list[UnderlyingTokenAmount]:
        self.abi.block = tokenamount.block  # TODO: improve this workarround
        amount_teu = self.abi.convert_to_assets(tokenamount.amount_teu)
        return [UnderlyingTokenAmount(token=self.unwrapped_token, amount_teu=amount_teu)]


SdaiToken(
    symbol="sDAI", chain=Chain.ETHEREUM, address="0x83F20F44975D03b1b09e64809B757c47f942BEeA", unwrapped_token=eth_DAI
)
SdaiToken(symbol="sDAI", chain=Chain.GNOSIS, address="0xaf204776c7245bF4147c2612BF6e5972Ee483701", unwrapped_token=xDAI)


class Position(Position):
    protocol: str = "maker"
    context: "Positions"
    address: str


class Vault(Position):
    id: int
    __repr__ = repr_for("address", "id", "underlyings", "unclaimed_rewards")


class DSR(Position):
    pass


class Pot(Position):
    pass


class Iou(Position):
    pass


class Positions(Frozen, KwInit):
    wallet: str
    chain: Blockchain
    block: int

    __repr__ = repr_for("wallet", "chain", "block")

    def __iter__(self) -> Iterator[Position]:
        yield from self.vaults
        if self.dsr:
            yield self.dsr
        if self.pot:
            yield self.pot
        if self.iou:
            yield self.iou

    @default
    def DAI(self):
        return ERC20Token.objs.get(chain=self.chain, symbol="DAI")

    @default
    def vaults(self) -> list[Vault]:
        cdp = contracts.CdpManager(self.chain, self.block)
        ilk_registry = contracts.IlkRegistry(self.chain, self.block)
        vat = contracts.Vat(self.chain, self.block)
        for vault_id in cdp.get_vault_ids(contracts.ProxyRegistry(self.chain, self.block).proxies(self.wallet)):
            ilk = cdp.ilks(vault_id)
            gem = ilk_registry.info(ilk)[4]
            urn_handler_address = cdp.urns(vault_id)
            ink, art = vat.urns(ilk, urn_handler_address)
            rate = vat.ilks(ilk)[1]

            lend_token = ERC20Token.objs.get_or_create(chain=self.chain, address=gem)
            yield Vault(
                address=cdp.contract.address,
                id=vault_id,
                context=self,
                underlyings=[
                    UnderlyingTokenAmount(token=lend_token, amount_teu=ink, block=self.block),
                    UnderlyingTokenAmount(token=self.DAI, amount_teu=-1 * art * rate, block=self.block),
                ],
                rate=rate,
            )

    @default
    def dsr(self) -> DSR:
        dsr = contracts.DsrManager(self.chain, self.block)
        return DSR(
            context=self,
            address=dsr.contract.address,
            underlyings=[UnderlyingTokenAmount(token=self.DAI, amount_teu=dsr.dai_balance(self.wallet))],
        )

    @default
    def pot(self) -> Pot:
        pot = contracts.Pot(self.chain, self.block)
        return Pot(
            context=self,
            address=pot.contract.address,
            underlyings=[UnderlyingTokenAmount(token=self.DAI, amount_teu=pot.pie_1(self.wallet) * pot.chi_decimal)],
        )

    @default
    def iou(self) -> Iou:
        iou = contracts.Iou(self.chain, self.block)
        MKR = ERC20Token.objs.get(chain=self.chain, symbol="MKR")
        return Iou(
            context=self,
            address=iou.contract.address,
            underlyings=[UnderlyingTokenAmount(token=MKR, amount_teu=iou.balance_of(self.wallet))],
        )
