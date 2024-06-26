import logging
from functools import cached_property
from typing import Iterator

from defabipedia import Blockchain, Chain
from defabipedia.tokens import EthereumTokenAddr
from karpatkit.helpers import listify

from defyes.portfolio import (
    DeployedToken,
    FrozenKwInit,
    NativeToken,
    Position,
    Token,
    TokenPosition,
    UnderlyingTokenPosition,
    Unwrappable,
    repr_for,
)

from . import contracts

logger = logging.getLogger(__name__)

xDAI = NativeToken.objs.get(chain=Chain.GNOSIS)

class Maker:
    protocol = "maker"


class MakerToken(Maker, DeployedToken):
    pass


class MakerDeployment(Maker, Deployment):
    pass


MakerToken.objs.create(symbol="MKR", chain=Chain.ETHEREUM, address=EthereumTokenAddr.MKR)
eth_DAI = MakerToken.objs.create(symbol="DAI", chain=Chain.ETHEREUM, address=EthereumTokenAddr.DAI)


# TODO: Move this to spark when spark will have the newarch.py
class SdaiToken(Unwrappable, DeployedToken):
    protocol = "spark"
    contract_class = contracts.Sdai
    unwrapped_token: Token

    def unwrap(self, token_position: TokenPosition) -> list[UnderlyingTokenPosition]:
        self.contract.block = token_position.block  # TODO: improve this workarround
        amount_teu = self.contract.convert_to_assets(token_position.amount_teu)
        return [UnderlyingTokenPosition(token=self.unwrapped_token, amount_teu=amount_teu, parent=token_position)]


SdaiToken.objs.create(
    symbol="sDAI", chain=Chain.ETHEREUM, address="0x83F20F44975D03b1b09e64809B757c47f942BEeA", unwrapped_token=eth_DAI
)
SdaiToken.objs.create(
    symbol="sDAI", chain=Chain.GNOSIS, address="0xaf204776c7245bF4147c2612BF6e5972Ee483701", unwrapped_token=xDAI
)


def create_from_defaul_addresses(deployed_unit_class):
    for chain, address in deployed_unit_class.contract_class.default_addresses.items():
        deployed_unit_class.objs.create(chain=chain, address=address)


@create_from_defaul_addresses
class CDPManager(Unwrappable, MakerDeployment):
    contract_class = contracts.CdpManager

    @listify
    def unwrap(self, position: Position) -> list[UnderlyingPosition]:
        ilk_registry = contracts.IlkRegistry(self.chain, position.block)
        vat = contracts.Vat(self.chain, position.block)
        proxy_addr = contracts.ProxyRegistry(self.chain, position.block).proxies(position.wallet)
        for vault_id in self.contract.get_vault_ids(proxy_addr):
            ilk = self.contract.ilks(vault_id)
            gem = ilk_registry.info(ilk)[4]
            urn_handler_address = self.contract.urns(vault_id)
            ink, art = vat.urns(ilk, urn_handler_address)
            rate = vat.ilks(ilk)[1]

            lend_token = DeployedToken.objs.get_or_create(chain=self.chain, address=gem)
            DAI = DeployedToken.objs.get(chain=self.chain, symbol="DAI")
            yield IdPosition(
                id=vault_id,
                unit=self,
                proxy_addr=proxy_addr,
                underlying=[
                    UnderlyingTokenPosition(unit=lend_token, amount_teu=ink, block=position.block),
                    UnderlyingTokenPosition(unit=DAI, amount_teu=-1 * art * rate, block=position.block),
                ],
                rate=rate,
            )


@create_from_defaul_addresses
class DSR(Unwrappable, MakerDeployment):
    contract_class = contracts.DsrManager
    name = "manager"

    @listify
    def unwrap(self, position: Position) -> list[UnderlyingPosition]:
        DAI = DeployedToken.objs.get(chain=self.chain, symbol="DAI")
        yield UnderlyingTokenPosition(unit=DAI, amount_teu=self.contract.dai_balance(position.wallet))



class MakerPosition(Maker, Position):
    pass


class Vault(MakerPosition):
    id: int
    __repr__ = repr_for("address", "id", "underlying", "unclaimed_rewards")


class DSRPot(MakerPosition):
    pass


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

    @cached_property
    def DAI(self):
        return DeployedToken.objs.get(chain=self.chain, symbol="DAI")

    @cached_property
    @listify
    def vaults(self) -> list[Vault]:
        # contracts = defabipedia.maker.ContractSpecs[self.chain]
        # node = get_node(self.chain)
        # cdp = contracts.CdpManager.contract(node)
        cdp = contracts.CdpManager(self.chain, self.block)
        ilk_registry = contracts.IlkRegistry(self.chain, self.block)
        vat = contracts.Vat(self.chain, self.block)
        for vault_id in cdp.get_vault_ids(self.proxy_addr):
            ilk = cdp.ilks(vault_id)
            gem = ilk_registry.info(ilk)[4]
            urn_handler_address = cdp.urns(vault_id)
            ink, art = vat.urns(ilk, urn_handler_address)
            rate = vat.ilks(ilk)[1]

            lend_token = DeployedToken.objs.get_or_create(chain=self.chain, address=gem)
            yield Vault(
                address=cdp.contract.address,
                proxy_addr=self.proxy_addr,
                id=vault_id,
                context=self,
                underlying=[
                    UnderlyingTokenPosition(token=lend_token, amount_teu=ink, block=self.block),
                    UnderlyingTokenPosition(token=self.DAI, amount_teu=-1 * art * rate, block=self.block),
                ],
                rate=rate,
            )

    @cached_property
    def proxy_addr(self) -> str:
        return contracts.ProxyRegistry(self.chain, self.block).proxies(self.wallet)

    @cached_property
    def dsr(self) -> DSR:
        dsr = contracts.DsrManager(self.chain, self.block)
        return DSR(
            context=self,
            address=dsr.contract.address,
            underlying=[UnderlyingTokenPosition(token=self.DAI, amount_teu=dsr.dai_balance(self.wallet))],
        )

    @cached_property
    def dsr_pot(self) -> DSRPot:
        pot = contracts.Pot(self.chain, self.block)
        return DSRPot(
            context=self,
            address=pot.contract.address,
            underlying=[UnderlyingTokenPosition(token=self.DAI, amount_teu=pot.pie_1(self.wallet) * pot.chi_decimal)],
        )

    @cached_property
    def iou(self) -> Iou:
        iou = contracts.Iou(self.chain, self.block)
        MKR = DeployedToken.objs.get(chain=self.chain, symbol="MKR")
        return Iou(
            context=self,
            address=iou.contract.address,
            underlying=[UnderlyingTokenPosition(token=MKR, amount_teu=iou.balance_of(self.wallet))],
        )
