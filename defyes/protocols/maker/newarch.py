import logging
from contextlib import suppress
from decimal import Decimal
from typing import Iterator, Tuple, Union

from defabipedia import Blockchain, Chain
from defabipedia.tokens import EthereumTokenAddr, GnosisTokenAddr
from web3 import Web3

from defyes.functions import balance_of, ensure_a_block_number
from defyes.porfolio import DeploymentCrypto, ERC20Token, Frozen, KwInit, NativeToken, Position, default, repr_for, Unwrappable, TokenAmount, UnderlyingTokenAmount, Token

from . import contracts

logger = logging.getLogger(__name__)

xDAI = NativeToken.instances.get(chain=Chain.GNOSIS)


class SdaiToken(Unwrappable, ERC20Token):
    abi_class = contracts.Sdai

    def unwrap(self, tokenamount: TokenAmount) -> UnderlyingTokenAmount:
        self.abi.block = tokenamount.block  # TODO: improve this workarround
        amount_teu = self.abi.convert_to_assets(tokenamount.amount_teu)
        return UnderlyingTokenAmount(token=self.unwrapped_token, amount_teu=amount_teu)


class tokens:
    class ethereum:
        MKR = ERC20Token(chain=Chain.ETHEREUM, address=EthereumTokenAddr.MKR)
        DAI = ERC20Token(chain=Chain.ETHEREUM, address=EthereumTokenAddr.DAI)
        sDAI = SdaiToken(
            chain=Chain.ETHEREUM, address="0x83F20F44975D03b1b09e64809B757c47f942BEeA", unwrapped_token=DAI
        )

    class gnosis:
        sDAI = SdaiToken(chain=Chain.GNOSIS, address="0xaf204776c7245bF4147c2612BF6e5972Ee483701", unwrapped_token=xDAI)


############################################################
############################################################
# def instanceof(class_):
#    return class_()
#
# class tokens:
#    class ethereum:
#        _ = partial(ERC20Token, chain=Chain.ETHEREUM)
#        MKR = _(address=EthereumTokenAddr.MKR)
#        DAI = _(address=EthereumTokenAddr.DAI)
#
#        @instanceof
#        class sDAI(ERC20Token):
#            chain = Chain.ETHEREUM
#            address = "0x83F20F44975D03b1b09e64809B757c47f942BEeA"
#            abi_class = abis.Sdai
#            unwrapped = DAI
#
#    class gnosis:
#        xDAI = NativeToken(chain=Chain.GNOSIS, symbol="xDAI")
#
#        @instanceof
#        class sDAI(ERC20Token):
#            chain = Chain.GNOSIS
#            address = "0xaf204776c7245bF4147c2612BF6e5972Ee483701"
#            unwrapped = xDAI
#
#            class abi_class(abis.Sdai):
#                dai = Address.ZERO


############################################################
############################################################

class Position(Position):
    protocol: str = "maker"


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

    class Vault(Position):
        id: int
        __repr__ = repr_for("id", "underlyings", "unclaimed_rewards")

    @default
    def DAI(self):
        return Token.instances.get(chain=self.chain, symbol="DAI")

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

            #lend_token = ERC20Token.instances.get_or_create(chain=self.chain, address=gem)
            try:
                lend_token = Token.instances.get(chain=self.chain, address=gem)
            except LookupError:
                lend_token = ERC20Token(chain=self.chain, address=gem)
                Token.instances.add(lend_token)
            yield self.Vault(
                id=vault_id,
                underlyings=[
                    UnderlyingTokenAmount(token=lend_token, amount_teu=ink, block=self.block),
                    UnderlyingTokenAmount(token=self.DAI, amount_teu=-1 * art * rate, block=self.block),
                ],
                rate=rate,
            )

    # class DsrManager(PositionType):
    #    abi_class = abis.DsrManager
    #    def pie_of(self, wallet: str) -> Decimal:
    #        return Decimal(self.abi.pie_of(wallet)).scaleb(-27)

    class Manager(Position):
        pass
        #@default
        #def underlyings(self):
        #    yield UnderlyingTokenAmount(token=self.DAI, amount=self.pie_of(self.wallet))

    @default
    def dsr(self) -> Manager:
        #dsr = contracts.DsrManagerDeployment()
        dsr = contracts.DsrManager(self.chain, self.block)
        return self.Manager(underlyings=[UnderlyingTokenAmount(token=self.DAI, amount=dsr.decimal_pie_of(self.wallet))])

    # @default
    # def dsr(self) -> Manager:
    #    dsr = DsrManager(chain=self.chain, block=self.block)
    #    yield self.Manager(underlyings=[UnderlyingTokenAmount(token=self.DAI, amount=dsr.decimal_pie_of(self.wallet))])

    class Pot(Position):
        pass

    @default
    def pot(self) -> Pot:
        pot = contracts.Pot(self.chain, self.block)
        return self.Pot(underlying=[UnderlyingTokenAmount(token=self.DAI, amount=pot.decimal_pie_1(self.wallet) * pot.chi)])

    class Iou(Position):
        pass

    @default
    def iou(self) -> Iou:
        iou = contracts.Iou(self.chain, self.block)
        MKR = Token.instances.get(chain=self.chain, symbol="MKR")
        return self.Iou(underlying=[UnderlyingTokenAmount(token=MKR, amount_teu=iou.balance_of(self.wallet))])
