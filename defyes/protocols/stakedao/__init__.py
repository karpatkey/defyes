from defabipedia import Chain
from web3 import Web3
from web3.exceptions import ContractLogicError

from defyes.functions import ensure_a_block_number
from defyes.types import Addr, Token, TokenAmount

from .autogenerated import Gauge, Operator, Sdtoken

# From https://github.com/stake-dao/address-book/tree/main/src/lockers
TOKEN_ADDRS = {
    Chain.ETHEREUM: [
        "0xD1b5651E55D4CeeD36251c61c50C889B36F6abB5",  # sdCRV
        "0x752B4c6e92d96467fE9b9a2522EF07228E00F87c",  # sdANGLE
        "0x26f01FE3BE55361b0643bc9d5D60980E37A2770D",  # sdSPECTRA
        "0xF24d8651578a55b0C119B9910759a351A3458895",  # sdBAL
        "0x825Ba129b3EA1ddc265708fcbB9dd660fdD2ef73",  # sdBPT
        "0x402F878BDd1f5C66FdAF0fabaBcF74741B68ac36",  # sdFXS
        "0x334cB66050049c1E392007B018321c44A1dbFaC4",  # sdFPIS
        "0x97983236bE88107Cc8998733Ef73D8d969c52E37",  # sdYFI
        "0x5Ea630e00D6eE438d3deA1556A110359ACdc10A9",  # sdPENDLE
        "0x50687515e93C43964733282F9DB8683F80BB02f9",  # sdMAV
        "0xe19d1c837B8A1C83A56cD9165b2c0256D39653aD",  # sdFXN
    ],
    Chain.BINANCE: [
        "0x6a1c1447F97B27dA23dC52802F5f1435b5aC821A",  # sdCAKE
        "0x50687515e93C43964733282F9DB8683F80BB02f9",  # sdMAV
    ],
    Chain.BASE: [
        "0x75289388d50364c3013583d97bd70cED0e183e32",  # sdMAV
    ],
}


class Gauge(Gauge):
    def get_rewards(self, wallet: str):
        rewards = []
        n = self.reward_count
        for n_reward in range(n):
            reward_token = self.reward_tokens(n_reward)
            balance = self.claimable_reward(wallet, reward_token)
            if balance:
                token = Token.get_instance(reward_token, self.blockchain, self.block)
                rewards.append(TokenAmount.from_teu(balance, token))
        return rewards


def get_protocol_data_for(
    blockchain: str,
    wallet: str,
    lptoken_address: str,
    block: int | str = "latest",
    decimals: bool = True,
) -> dict:
    wallet = Addr(Web3.to_checksum_address(wallet))
    lptoken_address = Web3.to_checksum_address(lptoken_address)
    block_id = ensure_a_block_number(block, blockchain)
    data = {"holdings": [], "underlyings": [], "unclaimed_rewards": [], "financial_metrics": {}}

    if lptoken_address not in TOKEN_ADDRS[blockchain]:
        raise ValueError(f"Wrong sdtoken provided ({lptoken_address}) for {blockchain}")

    sd_token = Sdtoken(blockchain, block_id, lptoken_address)
    try:
        operator_addr = sd_token.operator
    except ContractLogicError:
        operator_addr = sd_token.minter
    operator = Operator(blockchain, block_id, operator_addr)
    gauge = Gauge(blockchain, block_id, operator.gauge)

    sd_balance = gauge.balance_of(wallet)
    if sd_balance:
        htoken = Token.get_instance(gauge.staking_token, blockchain, block_id)
        data["holdings"] = [TokenAmount.from_teu(sd_balance, htoken)]
        # utoken = Token.get_instance(operator.token, blockchain, block_id)
        data["underlyings"] = [TokenAmount.from_teu(sd_balance, htoken)]
    data["unclaimed_rewards"] = gauge.get_rewards(wallet)

    return data
