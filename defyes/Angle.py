import logging
from decimal import Decimal
from typing import Dict, List

from web3 import Web3
from web3.exceptions import ContractCustomError, ContractLogicError

from defyes.cache import cache_contract_method
from defyes.constants import ETHEREUM
from defyes.contract import DefiContract
from defyes.functions import get_decimals

logger = logging.getLogger(__name__)


# Borrow Module
# https://docs.angle.money/angle-borrowing-module/borrowing-module
# https://github.com/AngleProtocol/borrow-contracts/tree/main
class Treasury(DefiContract):
    # https://developers.angle.money/borrowing-module-contracts/smart-contract-docs/treasury
    # https://github.com/AngleProtocol/borrow-contracts/tree/main/contracts/treasury
    ABI: str = """[{"inputs":[],\
                    "name":"stablecoin",\
                    "outputs":[{"internalType":"contract IAgToken","name":"","type":"address"}],\
                    "stateMutability":"view","type":"function"},\
                   {"inputs":[{"internalType":"uint256", "name":"","type":"uint256"}],\
                    "name":"vaultManagerList",\
                    "outputs":[{"internalType":"address","name":"","type":"address"}],\
                    "stateMutability":"view","type":"function"},\
                   {"inputs":[{"internalType":"address","name":"_vaultManager","type":"address"}],\
                    "name":"isVaultManager",\
                    "outputs":[{"internalType":"bool","name":"","type":"bool"}],\
                    "stateMutability":"view","type":"function"}\
                  ]"""
    ADDRS: Dict = {ETHEREUM: "0x8667DBEBf68B0BFa6Db54f550f41Be16c4067d60"}

    def __init__(self, blockchain) -> None:
        super().__init__(blockchain, self.ADDRS[blockchain])

    @property
    def stable_token(self):
        return self.stablecoin().const_call()

    def get_all_vault_managers_addrs(self, block) -> List[str]:
        """
        Returns all vault manager addresses from treasury.
        """
        nvault = 0
        vaults = []
        while True:
            try:
                vaults.append(self.vaultManagerList(nvault).call(block_identifier=block))
                nvault += 1
            except ContractLogicError as error:
                if error.message == "execution reverted":
                    logger.debug("End of vault manager list reachead")
                    break
                else:
                    raise ContractLogicError(error)
        return vaults


class Oracle(DefiContract):
    ABI: str = """[{"inputs": [],\
                    "name": "DESCRIPTION",\
                    "outputs": [{"internalType": "string", "name": "", "type": "string"}],\
                    "stateMutability": "view","type": "function"},\
                   {"inputs": [],\
                    "name": "read",\
                    "outputs": [{"internalType": "uint256", "name": "quoteAmount", "type": "uint256"}],\
                    "stateMutability": "view", "type": "function"}\
                  ]"""

    def __init__(self, blockchain, address) -> None:
        super().__init__(blockchain, address)
        self.decimals = self.get_decimals()

    def get_decimals(self) -> int:
        description = self.DESCRIPTION().const_call()
        if "EUR" in description:
            return 18
        else:
            raise ValueError("Not decimal specified")

    def rate(self, block) -> Decimal:
        return self.read().call(block_identifier=block) / Decimal(10**self.decimals)


class VaultManager(DefiContract):
    ABI: str = """[{"inputs": [{"internalType": "address", "name": "owner", "type": "address"}],\
                    "name": "balanceOf",\
                    "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],\
                    "stateMutability": "view", "type": "function"},\
                   {"inputs":[],\
                    "name":"vaultIDCount",\
                    "outputs":[{"internalType":"uint256","name":"","type":"uint256"}],\
                    "stateMutability":"view","type":"function"},\
                   {"inputs":[{"internalType":"uint256","name":"vaultID","type":"uint256"}],\
                    "name":"ownerOf",\
                    "outputs":[{"internalType":"address","name":"","type":"address"}],\
                    "stateMutability":"view","type":"function"},\
                   {"inputs":[],\
                    "name":"oracle",\
                    "outputs":[{"internalType":"contract IOracle","name":"","type":"address"}],\
                    "stateMutability":"view","type":"function"},\
                   {"inputs": [],\
                    "name": "collateralFactor",\
                    "outputs": [{"internalType": "uint64", "name": "", "type": "uint64"}],\
                    "stateMutability": "view", "type": "function"},\
                   {"inputs": [],\
                    "name": "BASE_INTEREST",\
                    "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                    "stateMutability": "view", "type": "function"},\
                   {"inputs": [],\
                    "name": "BASE_PARAMS",\
                    "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                    "stateMutability": "view", "type": "function"},\
                   {"inputs": [],\
                    "name": "collateral",\
                    "outputs": [{"internalType": "contract IERC20", "name": "", "type": "address"}],\
                    "stateMutability": "view", "type": "function"},\
                   {"inputs": [{"internalType": "uint256", "name": "vaultID", "type": "uint256"}],\
                    "name": "getVaultDebt",\
                    "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                    "stateMutability": "view", "type": "function"},\
                   {"inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],\
                    "name": "vaultData",\
                    "outputs": [{"internalType": "uint256", "name": "collateralAmount", "type": "uint256"},\
                                {"internalType": "uint256", "name": "normalizedDebt", "type": "uint256"}],\
                    "stateMutability": "view", "type": "function"},\
                   {"inputs":[],\
                    "name":"stablecoin",\
                    "outputs":[{"internalType":"contract IAgToken","name":"","type":"address"}],\
                    "stateMutability":"view","type":"function"},\
                   {"inputs": [],\
                    "name": "interestRate",\
                    "outputs": [{"internalType": "uint64", "name": "", "type": "uint64"}],\
                    "stateMutability": "view", "type": "function"}\
                  ]"""

    def __init__(self, blockchain, address) -> None:
        super().__init__(blockchain, address)

    def vaults_owned_by(self, wallet: str, block: int | str) -> int:
        wallet = Web3.to_checksum_address(wallet)
        return self.balanceOf(wallet).call(block_identifier=block)

    @property
    def stable_token(self):
        return self.stablecoin().const_call()

    @property
    def collateral_token(self):
        return self.collateral().const_call()

    def get_oracle(self) -> Oracle:
        return Oracle(self.blockchain, self.oracle().const_call())

    def get_vault_data(self, vaultid: int, block: int, decimals: bool = True) -> Dict:
        stablecoin_decimals = get_decimals(self.stable_token, self.blockchain, self.get_node(block)) if decimals else 0
        collateral_decimals = (
            get_decimals(self.collateral_token, self.blockchain, self.get_node(block)) if decimals else 0
        )
        contract_decimals = str(self.BASE_PARAMS().const_call()).count("0")
        interest_decimals = str(self.BASE_INTEREST().const_call()).count("0")

        collateral_factor = self.collateralFactor().call(block_identifier=block) / Decimal(10**contract_decimals)

        debt = self.getVaultDebt(vaultid).call(block_identifier=block) / Decimal(10**stablecoin_decimals)

        collateral_deposit, normalized_debt = self.vaultData(vaultid).call(block_identifier=block)
        collateral_amount = collateral_deposit / Decimal(10**collateral_decimals)

        collateral_to_stablecoin = self.get_oracle().rate(block)
        collateral_in_stablecoin = collateral_deposit * collateral_to_stablecoin / Decimal(10**stablecoin_decimals)

        # health_factor = collateral_in_stablecoin * collateral_factor / debt

        available_to_borrow = collateral_in_stablecoin * collateral_factor - debt

        interest_rate_per_second = self.interestRate().call(block_identifier=block) / Decimal(10**interest_decimals)

        data = {
            "assets": [
                {"address": self.stable_token, "balance": -debt},
                {"address": self.collateral_token, "balance": collateral_amount},
            ],
            "financial_metrics": {
                # "health_factor": health_factor,
                # "loan_to_value": debt / collateral_in_stablecoin,
                "collateral_ratio": collateral_in_stablecoin / debt,
                "liquidation_ratio": 1 / collateral_factor,
                "anual_interest_rate": interest_rate_per_second * 365 * 24 * 3600,
                "liquidation_price_in_stablecoin_fiat": debt / collateral_factor / collateral_amount,
                "available_to_borrow": {"address": self.stable_token, "balance": available_to_borrow},
            },
        }
        return data

    def vault_ids_owned_by(self, wallet: str, block: int | str, vault_ids: List) -> bool:
        if self.vaults_owned_by(wallet, block) != len(vault_ids):
            return False
        for vault_id in vault_ids:
            if self.ownerOf(vault_id).call(block_identifier=block) != wallet:
                return False
        return True

    @cache_contract_method(exclude_args=["block"], validator=vault_ids_owned_by)
    def get_vault_ids_from(self, wallet: str, block: int | str) -> List:
        wallet = Web3.to_checksum_address(wallet)
        vault_ids = []
        vaults = self.vaultIDCount().call(block_identifier=block)
        for vault_id in range(vaults + 1):
            try:
                if wallet == self.ownerOf(vault_id).call(block_identifier=block):
                    vault_ids.append(vault_id)
            except ContractCustomError as error:
                if error == "0x0c5473ba":
                    pass
                else:
                    ContractCustomError(error)
        return {"wallet": wallet, "block": block, "vault_ids": vault_ids}


def underlying(blockchain: str, wallet: str, block: int | str = "latest", decimals: bool = True) -> dict:
    """
    TODO: Add documentation
    """
    wallet = Web3.to_checksum_address(wallet)
    treasury = Treasury(blockchain)

    positions = {}

    for vault_addr in treasury.get_all_vault_managers_addrs(block):
        vault_manager = VaultManager(blockchain, vault_addr)
        if vault_manager.vaults_owned_by(wallet, block) >= 1:
            vault_ids = vault_manager.get_vault_ids_from(wallet, block)["vault_ids"]
            for vault_id in vault_ids:
                vault_data = vault_manager.get_vault_data(vault_id, block, decimals=decimals)
                positions[str(vault_id)] = vault_data
    return {
        "protocol": "Angle",
        "blockchain": blockchain,
        "block": block,
        "positions_key": "vault_id",
        "positions": positions,
        "underlying_version": 0,
    }
