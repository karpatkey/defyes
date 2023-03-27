from defi_protocols.functions import get_node, balance_of, total_supply, GetNodeIndexError
from defi_protocols.constants import MAX_EXECUTIONS, ETHEREUM



LPTOKENSDATABASE_ETH = [["Reflexer-FLX/WETH","0xd6F3768E62Ef92a9798E5A8cEdD2b78907cEceF9","0xd6F3768E62Ef92a9798E5A8cEdD2b78907cEceF9",["0x6243d8cea23066d098a15582d81a598b4e8391f4","0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"]]]
LPTOKENSDATABASE = LPTOKENSDATABASE_ETH

def lptoken_underlying(lptoken_address, amount, block, blockchain):
    web3 = get_node(blockchain, block=block)
    index = [LPTOKENSDATABASE[i][1].lower() for i in range(len(LPTOKENSDATABASE))].index(lptoken_address.lower())
    poolAddress = web3.to_checksum_address(LPTOKENSDATABASE[index][2])
    tokens = LPTOKENSDATABASE[index][3]
    fraction = amount / total_supply(web3.to_checksum_address(lptoken_address), block, blockchain)

    return [[tokens[i], fraction * balance_of(poolAddress, tokens[i], block, blockchain)] for i in range(len(tokens))]


def pool_balance(lptoken_address, block, blockchain):
    web3 = get_node(blockchain, block=block)
    lptoken_address = web3.to_checksum_address(lptoken_address)

    return lptoken_underlying(lptoken_address, total_supply(lptoken_address, block, blockchain), block, blockchain)


def balance_of_lptoken_underlying(address, lptoken_address, block, blockchain):
    web3 = get_node(blockchain, block=block)

    return lptoken_underlying(web3.to_checksum_address(lptoken_address),
                              balance_of(address, web3.to_checksum_address(lptoken_address), block, blockchain), block, blockchain)



def underlying(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0):

    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)

        lptoken_address = web3.to_checksum_address(lptoken_address)
        LPtoken = web3.to_checksum_address('0xd6F3768E62Ef92a9798E5A8cEdD2b78907cEceF9')

        stLPtoken = web3.to_checksum_address('0x353efac5cab823a41bc0d6228d7061e92cf9ccb0')
        LPtoken = web3.to_checksum_address('0xd6F3768E62Ef92a9798E5A8cEdD2b78907cEceF9')
        balance = balance_of(wallet, stLPtoken, block, ETHEREUM)
        tokens = lptoken_underlying(LPtoken, balance, block, ETHEREUM)

        return tokens

    except GetNodeIndexError:
        return underlying(wallet, lptoken_address, block, blockchain, index=0, execution=execution+1)

    except:
        return underlying(wallet, lptoken_address, block, blockchain, index=index+1, execution=execution)


#print(underlying('0x849d52316331967b6ff1198e5e32a0eb168d039d','0xd6F3768E62Ef92a9798E5A8cEdD2b78907cEceF9','latest', ETHEREUM))
