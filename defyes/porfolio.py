from dataclasses import dataclass
from functools import cached_property

from defabipedia import Blockchain, Chain

# from defabipedia.tokens import EthereumTokenAddr

frozendata = dataclass(frozen=True)


@frozendata
class Deploy:
    chain: Blockchain
    address: str
    deploy_block: int = None


class AssetManager(list):
    def add(self, obj):
        try:
            i = self.index(obj)
        except ValueError:
            self.append(obj)
        else:
            raise ValueError(f"Already defined instance (current:{self[i]}, new:{obj}")

    def __get__(self, instance, owner=None):
        if owner is Asset:
            return self
        else:
            return [ins for ins in self if isinstance(ins, owner)]

    def filter(self, **kwargs):
        for ins in self:
            if all(getattr(ins, attr, None) == value for attr, value in kwargs.items()):
                yield ins

    def __call__(self, **kwargs):
        return AssetManager(self.filter(**kwargs))

    def get(self, **kwargs):
        return next(self.filter(**kwargs))


@frozendata
class Asset:
    name: str
    symbol: str
    # price: "Fiat"

    instances = AssetManager()

    def __post_init__(self):
        Asset.instances.add(self)
        self.post_init()

    def post_init(self):
        """
        Override this method in subclasses instead of __post_init__.
        """

    def __hash__(self):
        return hash(self.symbol)


@frozendata
class Native(Asset):
    chain: Blockchain
    decimals: int = 18

    def __hash__(self):
        return self.chain.chain_id


ETH = Native(chain=Chain.ETHEREUM, symbol="ETH", name="Ether")
Native(chain=Chain.POLYGON, symbol="MATIC", name="Matic")


@frozendata
class Fiat(Asset):
    pass


Fiat(symbol="USD", name="US dollar")
Fiat(symbol="EUR", name="Euro")


@frozendata
class Token(Deploy, Asset):
    @cached_property
    def symbol(self) -> str:
        return self.contract.symbol

    @cached_property
    def name(self) -> str:
        return self.contract.name

    @property
    def price(self) -> Fiat:
        raise NotImplementedError

    @cached_property
    def decimals(self) -> int:
        return self.contract.decimals

    def __hash__(self):
        return hash((self.chain.chain.id, self.address))


# Token(chain=Chain.ETHEREUM, address=EthereumTokenAddr.DAI)


"""
    amount: Amount
    @property
    def amount(self) -> Amount:
        raise NotImplemented
Asset (like Unit) add
|- Token (ERC20) add Deploy
|- PositionClass add Deploy underlying:set[AssetAmount] unclaimed_rewards:set[AssetAmount]
|- ...
|- Native add FakeDeploy
|- Fiat
|- DelegatedNative add Native real_address:str
|- DelegatedToken add Token real_address:str
|- DelegatedAsset add Asset delegated:Asset
"""
