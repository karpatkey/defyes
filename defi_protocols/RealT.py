from typing import Union

from defi_protocols.functions import get_node, get_contract, GetNodeIndexError
from defi_protocols.constants import MAX_EXECUTIONS

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# RealT Token Address
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# RealT Token Address
TOKEN_CONTRACT_XDAI: str = '0x7349C9eaA538e118725a6130e0f8341509b9f8A0'

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# RealT token contract ABI - UNDERLYING_ASSET_ADDRESS, balanceOf, decimals
TOKEN_CONTRACT_ABI = '[{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"UNDERLYING_ASSET_ADDRESS","inputs":[]},\
                        {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"balanceOf","inputs":[{"type":"address","name":"user","internalType":"address"}]},\
                        {"type":"function","stateMutability":"view","outputs":[{"type":"uint8","name":"","internalType":"uint8"}],"name":"decimals","inputs":[]}]'


def underlying(wallet: str, block: Union[int,str], blockchain: str, web3=None, execution=1, index=0, decimals=True) -> list:
    if execution > MAX_EXECUTIONS:
        return None

    balances = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)
        token_contract = get_contract(TOKEN_CONTRACT_XDAI,blockchain,web3,abi=TOKEN_CONTRACT_ABI)
        balance_of = token_contract.functions.balanceOf(wallet).call(block_identifier=block)
        token_decimals = token_contract.functions.decimals().call()
        underlying_token = token_contract.functions.UNDERLYING_ASSET_ADDRESS().call()
        if decimals == True:
            balances.append([underlying_token,balance_of/(10**token_decimals)])
        else:
            balances.append([underlying_token,balance_of])
        return balances


    except GetNodeIndexError:
        return underlying(wallet, block, blockchain, decimals=decimals, index=0, execution=execution + 1)

    except:
        return underlying(wallet, block, blockchain, decimals=decimals, index=index + 1, execution=execution)
