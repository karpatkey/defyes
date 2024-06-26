"""
Autogenerated module. Don't change it manualy. Instead, import its classes into __init__.py or even derive them adding
extra methds.

# Inside __init__.py

from .autogenerated import EthVault

# Optionally
class EthVault(EthVault):
    ...
"""

from karpatkit.node import get_node
from web3 import Web3

from defyes.generator import load_abi


class EthVault:
    default_addresses: dict[str, str]

    def __init__(self, blockchain: str, block: int, address: str | None = None) -> None:
        self.block = block
        self.blockchain = blockchain
        if address:
            self.address = Web3.to_checksum_address(address)
        else:
            try:
                self.address = self.default_addresses[blockchain]
            except AttributeError as e:
                raise ValueError("No default_addresses defined when trying to guess the address.") from e
            except KeyError as e:
                raise ValueError(
                    f"{blockchain!r} not defined in default_addresses when trying to guess the address."
                ) from e
        node = get_node(blockchain)
        self.contract = node.eth.contract(address=self.address, abi=load_abi(__file__, "eth_vault.json"))

    @property
    def upgrade_interface_version(self) -> str:
        return self.contract.functions.UPGRADE_INTERFACE_VERSION().call(block_identifier=self.block)

    @property
    def admin(self) -> str:
        return self.contract.functions.admin().call(block_identifier=self.block)

    def calculate_exited_assets(
        self, receiver: str, position_ticket: int, timestamp: int, exit_queue_index: int
    ) -> tuple[int, int, int]:
        """
        Output: leftShares, claimedShares, claimedAssets
        """
        return self.contract.functions.calculateExitedAssets(
            receiver, position_ticket, timestamp, exit_queue_index
        ).call(block_identifier=self.block)

    @property
    def capacity(self) -> int:
        return self.contract.functions.capacity().call(block_identifier=self.block)

    def convert_to_assets(self, shares: int) -> int:
        """
        Output: assets
        """
        return self.contract.functions.convertToAssets(shares).call(block_identifier=self.block)

    def convert_to_shares(self, assets: int) -> int:
        """
        Output: shares
        """
        return self.contract.functions.convertToShares(assets).call(block_identifier=self.block)

    def deposit(self, receiver: str, referrer: str) -> int:
        """
        Output: shares
        """
        return self.contract.functions.deposit(receiver, referrer).call(block_identifier=self.block)

    @property
    def fee_percent(self) -> int:
        return self.contract.functions.feePercent().call(block_identifier=self.block)

    @property
    def fee_recipient(self) -> str:
        return self.contract.functions.feeRecipient().call(block_identifier=self.block)

    def get_exit_queue_index(self, position_ticket: int) -> int:
        return self.contract.functions.getExitQueueIndex(position_ticket).call(block_identifier=self.block)

    def get_shares(self, account: str) -> int:
        return self.contract.functions.getShares(account).call(block_identifier=self.block)

    @property
    def implementation(self) -> str:
        return self.contract.functions.implementation().call(block_identifier=self.block)

    def initialize(self, params: bytes):
        return self.contract.functions.initialize(params).call(block_identifier=self.block)

    @property
    def is_state_update_required(self) -> bool:
        return self.contract.functions.isStateUpdateRequired().call(block_identifier=self.block)

    @property
    def keys_manager(self) -> str:
        return self.contract.functions.keysManager().call(block_identifier=self.block)

    @property
    def mev_escrow(self) -> str:
        return self.contract.functions.mevEscrow().call(block_identifier=self.block)

    def os_token_positions(self, user: str) -> int:
        """
        Output: shares
        """
        return self.contract.functions.osTokenPositions(user).call(block_identifier=self.block)

    @property
    def proxiable_uuid(self) -> bytes:
        return self.contract.functions.proxiableUUID().call(block_identifier=self.block)

    @property
    def queued_shares(self) -> int:
        return self.contract.functions.queuedShares().call(block_identifier=self.block)

    @property
    def receive_from_mev_escrow(self):
        return self.contract.functions.receiveFromMevEscrow().call(block_identifier=self.block)

    @property
    def total_assets(self) -> int:
        return self.contract.functions.totalAssets().call(block_identifier=self.block)

    @property
    def total_shares(self) -> int:
        return self.contract.functions.totalShares().call(block_identifier=self.block)

    def update_state_and_deposit(self, receiver: str, referrer: str, harvest_params: tuple) -> int:
        """
        Output: shares
        """
        return self.contract.functions.updateStateAndDeposit(receiver, referrer, harvest_params).call(
            block_identifier=self.block
        )

    def upgrade_to_and_call(self, new_implementation: str, data: bytes):
        return self.contract.functions.upgradeToAndCall(new_implementation, data).call(block_identifier=self.block)

    @property
    def validator_index(self) -> int:
        return self.contract.functions.validatorIndex().call(block_identifier=self.block)

    @property
    def validators_root(self) -> bytes:
        return self.contract.functions.validatorsRoot().call(block_identifier=self.block)

    @property
    def vault_id(self) -> bytes:
        return self.contract.functions.vaultId().call(block_identifier=self.block)

    @property
    def version(self) -> int:
        return self.contract.functions.version().call(block_identifier=self.block)

    @property
    def withdrawable_assets(self) -> int:
        return self.contract.functions.withdrawableAssets().call(block_identifier=self.block)
