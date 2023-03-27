from defi_protocols.functions import get_node, get_contract, GetNodeIndexError
from defi_protocols.constants import MAX_EXECUTIONS


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# LITERALS
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Contracts for calling liquidity pools and underlying tokens
BASIC_META_VAULT = '0x6d68f5b8c22a549334ca85960978f9de4deba2d3'



#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Network ABI - asset, assetPoolindex, assetScale, balanceOf, convertToAssets, decimals

BASIC_META_VAULT_ABI = '[{"inputs":[],"name":"asset","outputs":[{"internalType":"address","name":"assetTokenAddress","type":"address"}],"stateMutability":"view","type":"function"},\
                        {"inputs":[],"name":"assetPoolIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
                        {"inputs":[],"name":"assetScale","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
                        {"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
                        {"inputs":[{"internalType":"uint256","name":"shares","type":"uint256"}],"name":"convertToAssets","outputs":[{"internalType":"uint256","name":"assets","type":"uint256"}],"stateMutability":"view","type":"function"},\
                        {"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"decimals_","type":"uint8"}],"stateMutability":"view","type":"function"}]'


def underlying(token_address: str, wallet: str, block: int, blockchain: str, web3=None, execution=1, index=0, decimals=True, reward=False) -> list:
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    balances = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)
        token_address = web3.to_checksum_address(token_address)
        meta_vault_contract = get_contract(token_address,blockchain,web3=web3,abi=BASIC_META_VAULT_ABI,block=block)
        balance_of_vault = meta_vault_contract.functions.balanceOf(wallet).call(block_identifier=block)
        underlying_asset = meta_vault_contract.functions.asset().call()
        asset_scale = meta_vault_contract.functions.assetScale().call()
        balance_of_assets = meta_vault_contract.functions.convertToAssets(balance_of_vault).call()
        if decimals == True:
            balances.append([underlying_asset, balance_of_assets/asset_scale])
        else:
            balances.append([underlying_asset, balance_of_assets])
        return balances

    except GetNodeIndexError:
        return underlying(token_address, wallet, block, blockchain, web3=None, execution=execution+1, index=0)

    except:
        return underlying(token_address, wallet, block, blockchain, web3=None, execution=execution, index=index+1)     


# wallet = '0x83dE1603DF0249c0155e30c636598FEE5E11DBdc'
# token_address = '0x455fb969dc06c4aa77e7db3f0686cc05164436d2'
# test = underlying(token_address,wallet,'latest',ETHEREUM)
# print(test)
