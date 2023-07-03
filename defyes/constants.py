import json
import os
from pathlib import Path

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# BLOCKCHAINS
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
ETHEREUM = "ethereum"
POLYGON = "polygon"
XDAI = "xdai"
ARBITRUM = "arbitrum"
BINANCE = "binance"
AVALANCHE = "avalanche"
FANTOM = "fantom"
OPTIMISM = "optimism"
AVAX = "avax"
ROPSTEN = "ropsten"
KOVAN = "kovan"
GOERLI = "goerli"

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# NODES
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if "CONFIG_PATH" in os.environ:
    config_path = os.environ["CONFIG_PATH"]
    with open(config_path, "r") as config_file:
        config_data = json.load(config_file)
else:
    with open(str(Path(os.path.abspath(__file__)).resolve().parents[0]) + "/config.json", "r") as config_file:
        config_data = json.load(config_file)

NODE_ETH = {"latest": config_data["nodes"][ETHEREUM]["latest"], "archival": config_data["nodes"][ETHEREUM]["archival"]}

NODE_POL = {"latest": config_data["nodes"][POLYGON]["latest"], "archival": config_data["nodes"][POLYGON]["archival"]}

NODE_XDAI = {"latest": config_data["nodes"][XDAI]["latest"], "archival": config_data["nodes"][XDAI]["archival"]}

NODE_BINANCE = {
    "latest": config_data["nodes"][BINANCE]["latest"],
    "archival": config_data["nodes"][BINANCE]["archival"],
}

NODE_AVALANCHE = {
    "latest": config_data["nodes"][AVALANCHE]["latest"],
    "archival": config_data["nodes"][AVALANCHE]["archival"],
}

NODE_FANTOM = {"latest": config_data["nodes"][FANTOM]["latest"], "archival": config_data["nodes"][FANTOM]["archival"]}

NODE_OPTIMISM = {
    "latest": config_data["nodes"][OPTIMISM]["latest"],
    "archival": config_data["nodes"][OPTIMISM]["archival"],
}

NODE_ARBITRUM = {
    "latest": config_data["nodes"][ARBITRUM]["latest"],
    "archival": config_data["nodes"][ARBITRUM]["archival"],
}

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TESTNETS
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
NODE_ROPSTEN = {
    "latest": config_data["nodes"][ROPSTEN]["latest"],
    "archival": config_data["nodes"][ROPSTEN]["archival"],
}

NODE_KOVAN = {"latest": config_data["nodes"][KOVAN]["latest"], "archival": config_data["nodes"][KOVAN]["archival"]}

NODE_GOERLI = {"latest": config_data["nodes"][GOERLI]["latest"], "archival": config_data["nodes"][GOERLI]["archival"]}

NODES_ENDPOINTS = {
    ETHEREUM: NODE_ETH,
    POLYGON: NODE_POL,
    XDAI: NODE_XDAI,
    BINANCE: NODE_BINANCE,
    AVALANCHE: NODE_AVALANCHE,
    FANTOM: NODE_FANTOM,
    OPTIMISM: NODE_OPTIMISM,
    ROPSTEN: NODE_ROPSTEN,
    KOVAN: NODE_KOVAN,
    GOERLI: NODE_GOERLI,
    ARBITRUM: NODE_ARBITRUM,
}
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# MAX EXECUTIONS
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Maximum number of executions with different RPC endpoints, for a given function, in case of getting Unexpected Exceptions
MAX_EXECUTIONS = 2

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TESTNET HEADER
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Etherscan blocks requests that don't provide a User-Agent Hearder for Testnets.
TESTNET_HEADER = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Mobile Safari/537.36"
}

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ERC-20
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# GENERAL
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ALL ZEROS ADDRESS
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
# ALL E ADDRESS
E_ADDRESS = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
# ABI Token Simplified - name, symbol, SYMBOL, decimals, balanceOf, totalSupply
ABI_TOKEN_SIMPLIFIED = '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"}, {"constant":true,"inputs":[],"name":"SYMBOL","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]'

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ETHEREUM - Token Addresses
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
AURA_ETH = "0xC0c293ce456fF0ED870ADd98a0828Dd4d2903DBF"
AAVE_ETH = "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9"
ABPT_ETH = "0x41A08648C3766F9F9d85598fF102a08f4ef84F84"
B_80BAL_20_WETH_ETH = "0x5c6Ee304399DBdB9C8Ef030aB642B10820DB8F56"
BAL_ETH = "0xba100000625a3754423978a60c9317c58a424e3D"
BB_A_USD_OLD_ETH = "0x7B50775383d3D6f0215A8F290f2C9e2eEBBEceb2"
BB_A_USD_ETH = "0xA13a9247ea42D743238089903570127DdA72fE44"
COMP_ETH = "0xc00e94Cb662C3520282E6f5717214004A7f26888"
COW_ETH = "0xDEf1CA1fb7FBcDC777520aa7f396b4E015F497aB"
CRV_ETH = "0xD533a949740bb3306d119CC777fa900bA034cd52"
CRV_FRAX_ETH = "0x3175Df0976dFA876431C2E9eE6Bc45b65d3473CC"
CVX_ETH = "0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B"
CVXCRV_ETH = "0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7"
DAI_ETH = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
GNO_ETH = "0x6810e776880C02933D47DB1b9fc05908e5386b96"
LDO_ETH = "0x5A98FcBEA516Cf06857215779Fd812CA3beF1B32"
RETH2_ETH = "0x20BC832ca081b91433ff6c17f85701B6e92486c5"
SETH2_ETH = "0xFe2e637202056d30016725477c5da089Ab0A043A"
SNOTE_ETH = "0x38DE42F4BA8a35056b33A746A6b45bE9B1c3B9d2"
STETH_ETH = "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84"
SUSHI_ETH = "0x6B3595068778DD592e39A122f4f5a5cF09C90fE2"
STKAAVE_ETH = "0x4da27a545c0c5B758a6BA100e3a049001de870f5"
SWISE_ETH = "0x48C3399719B582dD63eB5AADf12A40B4C3f52FA2"
USDT_ETH = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
USDC_ETH = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
WBTC_ETH = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"
WETH_ETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
WSTETH_ETH = "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0"
X3CRV_ETH = "0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490"


class ETHTokenAddr:
    BAT = "0x0D8775F648430679A709E98d2b0Cb6250d2887EF"
    COW = "0xDEf1CA1fb7FBcDC777520aa7f396b4E015F497aB"
    DAI = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
    REP = "0x1985365e9f78359a9B6AD760e32412f4a445E862"
    USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
    USDT = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
    ZRX = "0xE41d2489571d322189246DaFA5ebDe1F4699F498"
    SAI = "0x89d24A6b4CcB1B6fAA2625fE562bDD9a23260359"
    UNI = "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"
    COMP = "0xc00e94Cb662C3520282E6f5717214004A7f26888"
    IDLE = "0x875773784Af8135eA0ef43b5a374AaD105c5D39e"
    WBTC = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"
    TUSD = "0x0000000000085d4780B73119b644AE5ecd22b376"
    LINK = "0x514910771AF9Ca656af840dff83E8264EcF986CA"
    MKR = "0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2"
    SUSHI = "0x6B3595068778DD592e39A122f4f5a5cF09C90fE2"
    AAVE = "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9"
    YFI = "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e"
    USDP = "0x8E870D67F660D95d5be530380D0eC0bd388289E1"
    FEI = "0x956F47F50A910163D8BF957Cf5846D573E7f87CA"
    BAL = "0xba100000625a3754423978a60c9317c58a424e3D"
    BB_A_USD_OLD = "0x7B50775383d3D6f0215A8F290f2C9e2eEBBEceb2"
    BB_A_USD = "0xA13a9247ea42D743238089903570127DdA72fE44"
    LDO = "0x5A98FcBEA516Cf06857215779Fd812CA3beF1B32"
    WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    AURA = "0xC0c293ce456fF0ED870ADd98a0828Dd4d2903DBF"
    auraBAL = "0x616e8BfA43F920657B3497DBf40D6b1A02D4608d"
    wstETH = "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0"
    stETH = "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84"
    OHM = "0x64aa3364F17a4D01c6f1751Fd97C2BD3D7e7f1D5"
    NOTE = "0xCFEAead4947f0705A14ec42aC3D44129E1Ef3eD5"
    GNO = "0x6810e776880C02933D47DB1b9fc05908e5386b96"
    sETH2 = "0xFe2e637202056d30016725477c5da089Ab0A043A"
    BNT = "0x1F573D6Fb3F13d689FF844B4cE37794d79a7FF1C"
    ICHI = "0x903bEF1736CDdf2A537176cf3C64579C3867A881"
    ABPT = "0x41A08648C3766F9F9d85598fF102a08f4ef84F84"
    ELK = "0xd8BaB53373B732Da40A7239359F141935dC00BfD"
    FLX = "0x6243d8CEA23066d098a15582d81a598b4e8391F4"
    STETH = "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84"


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# XDAI - Token Addresses
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
AGVE_XDAI = "0x3a97704a1b25F08aa230ae53B352e2e72ef52843"
BAL_XDAI = "0x7eF541E2a22058048904fE5744f9c7E4C57AF717"
COW_XDAI = "0x177127622c4A00F3d409B75571e12cB3c8973d3c"
CRV_XDAI = "0x712b3d230F3C1c19db860d80619288b1F0BDd0Bd"
GNO_XDAI = "0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb"
STKAGAVE_XDAI = "0x610525b415c1BFAeAB1a3fc3d85D87b92f048221"
WETH_XDAI = "0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1"
X3CRV_XDAI = "0x1337BedC9D22ecbe766dF105c9623922A27963EC"
WXDAI = "0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d"


class GnosisTokenAddr:
    AGVE = "0x3a97704a1b25F08aa230ae53B352e2e72ef52843"
    BAL = "0x7eF541E2a22058048904fE5744f9c7E4C57AF717"
    COW = "0x177127622c4A00F3d409B75571e12cB3c8973d3c"
    CRV = "0x712b3d230F3C1c19db860d80619288b1F0BDd0Bd"
    GNO = "0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb"
    nextDAI = "0x0e1D5Bcd2Ac5CF2f71841A9667afC1E995CaAf4F"
    nextUSDC = "0x44CF74238d840a5fEBB0eAa089D05b763B73faB8"
    nextUSDT = "0xF4d944883D6FddC56d3534986feF82105CaDbfA1"
    nextWETH = "0x538E2dDbfDf476D24cCb1477A518A82C9EA81326"
    STKAGAVE = "0x610525b415c1BFAeAB1a3fc3d85D87b92f048221"
    USDC = "0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83"
    USDT = "0x4ECaBa5870353805a9F068101A40E0f32ed605C6"
    WETH = "0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1"
    WXDAI = "0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d"
    X3CRV = "0x1337BedC9D22ecbe766dF105c9623922A27963EC"
    XGT = "0xC25AF3123d2420054c8fcd144c21113aa2853F39"
    ELK = "0xE1C110E1B1b4A1deD0cAf3E42BfBdbB7b5d7cE1C"
    SYMM = "0xC45b3C1c24d5F54E7a2cF288ac668c74Dd507a84"
    MAI = "0x3F56e0c36d275367b8C502090EDF38289b3dEa0d"


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# POLYGON - Token Addresses
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
BAL_POL = "0x9a71012B13CA4d3D0Cdc72A177DF3ef03b0E76A3"
MAI_POL = "0xa3Fa99A148fA48D14Ed51d610c367C61876997F1"
X3CRV_POL = "0xE7a24EF0C5e95Ffb0f6684b813A78F2a3AD7D171"


class PolygonTokenAddr:
    BAL = "0x9a71012B13CA4d3D0Cdc72A177DF3ef03b0E76A3"
    MAI = "0xa3Fa99A148fA48D14Ed51d610c367C61876997F1"
    X3CRV = "0xE7a24EF0C5e95Ffb0f6684b813A78F2a3AD7D171"
    USDC = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
    WETH = "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619"
    ELK = "0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE"


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ARBITRUM - Token Addresses
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
BAL_ARB = "0x040d1EdC9569d4Bab2D15287Dc5A4F10F56a56B8"

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# PROTOCOLS
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
AAVE = "Aave"
AGAVE = "Agave"
AURA = "Aura"
BALANCER = "Balancer"
CONVEX = "Convex"
CURVE = "Curve"
ELK = "Elk"
HONEYSWAP = "Honeyswap"
MAKER = "Maker"
QIDAO = "QiDao"
SUSHISWAP = "SushiSwap"
SWAPR = "Swapr"
SYMMETRIC = "Symmetric"
UNIT = "Unit"

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# API KEYS
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
API_KEY_ETHERSCAN = config_data["apikeys"]["etherscan"]
API_KEY_POLSCAN = config_data["apikeys"]["polscan"]
API_KEY_GNOSISSCAN = config_data["apikeys"]["gnosisscan"]
API_KEY_BINANCE = config_data["apikeys"]["binance"]
API_KEY_AVALANCHE = config_data["apikeys"]["avalanche"]
API_KEY_FANTOM = config_data["apikeys"]["fantom"]
API_KEY_OPTIMISM = config_data["apikeys"]["optimism"]
API_KEY_ARBITRUM = config_data["apikeys"]["arbitrum"]
API_KEY_ZAPPER = config_data["apikeys"]["zapper"]
API_KEY_ETHPLORER = config_data["apikeys"]["ethplorer"]

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# API CALLS
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# COINGECKO
API_COINGECKO_COINID_PRICE_RANGE = (
    "https://api.coingecko.com/api/v3/coins/%s/market_chart/range?vs_currency=usd&from=%d&to=%d"
)
API_COINGECKO_BLOCKCHAINID_TOKENADDRESS_PRICE_RANGE = (
    "https://api.coingecko.com/api/v3/coins/%s/contract/%s/market_chart/range?vs_currency=usd&from=%d&to=%d"
)
API_COINGECKO_BLOCKCHAINID_TOKENADDRESS_PRICE = "https://api.coingecko.com/api/v3/coins/%s/contract/%s"

# ZAPPER
API_ZAPPER_PRICE = "https://api.zapper.fi/v2/prices/%s?network=%s&timeFrame=%s&currency=USD&api_key=%s"

# SCANS - MODULE = BLOCKS - GETBLOCKNOBYTIME
API_ETHERSCAN_GETBLOCKNOBYTIME = (
    "https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp=%d&closest=before&apikey=%s"
)
API_POLYGONSCAN_GETBLOCKNOBYTIME = (
    "https://api.polygonscan.com/api?module=block&action=getblocknobytime&timestamp=%d&closest=before&apikey=%s"
)
API_GNOSISSCAN_GETBLOCKNOBYTIME = (
    "https://api.gnosisscan.io/api?module=block&action=getblocknobytime&timestamp=%d&closest=before&apikey=%s"
)
API_BLOCKSCOUT_GETBLOCKNOBYTIME = (
    "https://blockscout.com/xdai/mainnet/api?module=block&action=getblocknobytime&timestamp=%d&closest=before"
)
API_BINANCE_GETBLOCKNOBYTIME = (
    "https://api.bscscan.com/api?module=block&action=getblocknobytime&timestamp=%d&closest=before&apikey=%s"
)
API_AVALANCHE_GETBLOCKNOBYTIME = (
    "https://api.snowtrace.io/api?module=block&action=getblocknobytime&timestamp=%d&closest=before&apikey=%s"
)
API_FANTOM_GETBLOCKNOBYTIME = (
    "https://api.ftmscan.com/api?module=block&action=getblocknobytime&timestamp=%d&closest=before&apikey=%s"
)
API_OPTIMISM_GETBLOCKNOBYTIME = (
    "https://api-optimistic.etherscan.io/api?module=block&action=getblocknobytime&timestamp=%d&closest=before&apikey=%s"
)
API_ARBITRUM_GETBLOCKNOBYTIME = (
    "https://api.arbiscan.io/api?module=block&action=getblocknobytime&timestamp=%d&closest=before&apikey=%s"
)
API_ROPSTEN_GETBLOCKNOBYTIME = (
    "https://api-ropsten.etherscan.io/api?module=block&action=getblocknobytime&timestamp=%d&closest=before&apikey=%s"
)
API_KOVAN_GETBLOCKNOBYTIME = (
    "https://api-kovan.etherscan.io/api?module=block&action=getblocknobytime&timestamp=%d&closest=before&apikey=%s"
)
API_GOERLI_GETBLOCKNOBYTIME = (
    "https://api-goerli.etherscan.io/api?module=block&action=getblocknobytime&timestamp=%d&closest=before&apikey=%s"
)

# SCANS - MODULE = BLOCKS - GETBLOCKREWARD
API_ETHERSCAN_GETBLOCKREWARD = "https://api.etherscan.io/api?module=block&action=getblockreward&blockno=%d&apikey=%s"
API_POLYGONSCAN_GETBLOCKREWARD = (
    "https://api.polygonscan.com/api?module=block&action=getblockreward&blockno=%d&apikey=%s"
)
API_GNOSISSCAN_GETBLOCKREWARD = "https://api.gnosisscan.io/api?module=block&action=getblockreward&blockno=%d&apikey=%s"
API_BLOCKSCOUT_GETBLOCKREWARD = "https://blockscout.com/xdai/mainnet/api?module=block&action=getblockreward&blockno=%d"
API_BINANCE_GETBLOCKREWARD = "https://api.bscscan.com/api?module=block&action=getblockreward&blockno=%d&apikey=%s"
API_AVALANCHE_GETBLOCKREWARD = "https://api.snowtrace.io/api?module=block&action=getblockreward&blockno=%d&apikey=%s"
API_FANTOM_GETBLOCKREWARD = "https://api.ftmscan.com/api?module=block&action=getblockreward&blockno=%d&apikey=%s"
API_OPTIMISM_GETBLOCKREWARD = (
    "https://api-optimistic.etherscan.io/api?module=block&action=getblockreward&blockno=%d&apikey=%s"
)
API_ARBITRUM_GETBLOCKREWARD = "https://api.arbiscan.io/api?module=block&action=getblockreward&blockno=%d&apikey=%s"
API_ROPSTEN_GETBLOCKREWARD = (
    "https://api-ropsten.etherscan.io/api?module=block&action=getblockreward&blockno=%d&apikey=%s"
)
API_KOVAN_GETBLOCKREWARD = "https://api-kovan.etherscan.io/api?module=block&action=getblockreward&blockno=%d&apikey=%s"
API_GOERLI_GETBLOCKREWARD = (
    "https://api-goerli.etherscan.io/api?module=block&action=getblockreward&blockno=%d&apikey=%s"
)

# SCANS - MODULE = CONTRACTS - GETABI
API_ETHERSCAN_GETABI = "https://api.etherscan.io/api?module=contract&action=getabi&address=%s&apikey=%s"
API_POLYGONSCAN_GETABI = "https://api.polygonscan.com/api?module=contract&action=getabi&address=%s&apikey=%s"
API_GNOSISSCAN_GETABI = "https://api.gnosisscan.io/api?module=contract&action=getabi&address=%s&apikey=%s"
API_BLOCKSCOUT_GETABI = "https://blockscout.com/xdai/mainnet/api?module=contract&action=getabi&address=%s"
API_BINANCE_GETABI = "https://api.bscscan.com/api?module=contract&action=getabi&address=%s&apikey=%s"
API_AVALANCHE_GETABI = "https://api.snowtrace.io/api?module=contract&action=getabi&address=%s&apikey=%s"
API_FANTOM_GETABI = "https://api.ftmscan.com/api?module=contract&action=getabi&address=%s&apikey=%s"
API_OPTIMISM_GETABI = "https://api-optimistic.etherscan.io/api?module=contract&action=getabi&address=%s&apikey=%s"
API_ARBITRUM_GETABI = "https://api.arbiscan.io/api?module=contract&action=getabi&address=%s&apikey=%s"
API_ROPSTEN_GETABI = "https://api-ropsten.etherscan.io/api?module=contract&action=getabi&address=%s&apikey=%s"
API_KOVAN_GETABI = "https://api-kovan.etherscan.io/api?module=contract&action=getabi&address=%s&apikey=%s"
API_GOERLI_GETABI = "https://api-goerli.etherscan.io/api?module=contract&action=getabi&address=%s&apikey=%s"

# SCANS - MODULE = CONTRACTS - GETCONTRACTCREATION
API_ETHERSCAN_GETCONTRACTCREATION = (
    "https://api.etherscan.io/api?module=contract&action=getcontractcreation&contractaddresses=%s&apikey=%s"
)


# SCANS - MODULE = ACCOUNTS - TOKENTX
API_ETHERSCAN_TOKENTX = "https://api.etherscan.io/api?module=account&action=tokentx&contractaddress=%s&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s"
API_POLYGONSCAN_TOKENTX = "https://api.polygonscan.com/api?module=account&action=tokentx&contractaddress=%s&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s"
API_GNOSISSCAN_TOKENTX = "https://api.gnosisscan.io/api?module=account&action=tokentx&contractaddress=%s&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s"
API_BLOCKSCOUT_TOKENTX = "https://blockscout.com/xdai/mainnet/api?module=account&action=tokentx&contractaddress=%s&address=%s&startblock=%s&endblock=%s&sort=desc"
API_BINANCE_TOKENTX = "https://api.bscscan.com/api?module=account&action=tokentx&contractaddress=%s&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s"
API_AVALANCHE_TOKENTX = "https://api.snowtrace.io/api?module=account&action=tokentx&contractaddress=%s&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s"
API_FANTOM_TOKENTX = "https://api.ftmscan.com/api?module=account&action=tokentx&contractaddress=%s&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s"
API_OPTIMISM_TOKENTX = "https://api-optimistic.etherscan.io/api?module=account&action=tokentx&contractaddress=%s&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s"
API_ARBITRUM_TOKENTX = "https://api.arbiscan.io/api?module=account&action=tokentx&contractaddress=%s&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s"
API_ROPSTEN_TOKENTX = "https://api-ropsten.etherscan.io/api?module=account&action=tokentx&contractaddress=%s&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s"
API_KOVAN_TOKENTX = "https://api-kovan.etherscan.io/api?module=account&action=tokentx&contractaddress=%s&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s"
API_GOERLI_TOKENTX = "https://api-goerli.etherscan.io/api?module=account&action=tokentx&contractaddress=%s&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s"

# SCANS - MODULE = ACCOUNTS - TXLIST
API_ETHERSCAN_TXLIST = (
    "https://api.etherscan.io/api?module=account&action=txlist&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s"
)
API_POLYGONSCAN_TXLIST = "https://api.polygonscan.com/api?module=account&action=txlist&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s"
API_GNOSISSCAN_TXLIST = "https://api.gnosisscan.io/api?module=account&action=txlist&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s"
API_BLOCKSCOUT_TXLIST = "https://blockscout.com/xdai/mainnet/api?module=account&action=txlist&address=%s&startblock=%s&endblock=%s&sort=desc"
API_BINANCE_TXLIST = (
    "https://api.bscscan.com/api?module=account&action=txlist&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s"
)
API_AVALANCHE_TXLIST = (
    "https://api.snowtrace.io/api?module=account&action=txlist&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s"
)
API_FANTOM_TXLIST = (
    "https://api.ftmscan.com/api?module=account&action=txlist&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s"
)
API_OPTIMISM_TXLIST = "https://api-optimistic.etherscan.io/api?module=account&action=txlist&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s"
API_ARBITRUM_TXLIST = (
    "https://api.arbiscan.io/api?module=account&action=txlist&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s"
)
API_ROPSTEN_TXLIST = "https://api-ropsten.etherscan.io/api?module=account&action=txlist&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s"
API_KOVAN_TXLIST = "https://api-kovan.etherscan.io/api?module=account&action=txlist&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s"
API_GOERLI_TXLIST = "https://api-goerli.etherscan.io/api?module=account&action=txlist&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s"

# SCANS - MODULE = LOGS - GETLOGS
API_ETHERSCAN_GETLOGS = (
    "https://api.etherscan.io/api?module=logs&action=getLogs&fromBlock=%s&toBlock=%s&address=%s&topic0=%s&apikey=%s"
)
API_POLYGONSCAN_GETLOGS = (
    "https://api.polygonscan.com/api?module=logs&action=getLogs&fromBlock=%s&toBlock=%s&address=%s&topic0=%s&apikey=%s"
)
API_GNOSISSCAN_GETLOGS = (
    "https://api.gnosisscan.io/api?module=logs&action=getLogs&fromBlock=%s&toBlock=%s&address=%s&topic0=%s&apikey=%s"
)
API_BLOCKSCOUT_GETLOGS = (
    "https://blockscout.com/xdai/mainnet/api?module=logs&action=getLogs&fromBlock=%s&toBlock=%s&address=%s&topic0=%s"
)
API_AVALANCHE_GETLOGS = (
    "https://api.snowtrace.io/api?module=logs&action=getLogs&fromBlock=%s&toBlock=%s&address=%s&topic0=%s&apikey=%s"
)
API_BINANCE_GETLOGS = (
    "https://api.bscscan.com/api?module=logs&action=getLogs&fromBlock=%s&toBlock=%s&address=%s&topic0=%s&apikey=%s"
)
API_FANTOM_GETLOGS = (
    "https://api.ftmscan.com/api?module=logs&action=getLogs&fromBlock=%s&toBlock=%s&address=%s&topic0=%s&apikey=%s"
)
API_OPTIMISM_GETLOGS = "https://api-optimistic.etherscan.io/api?module=logs&action=getLogs&fromBlock=%s&toBlock=%s&address=%s&topic0=%s&apikey=%s"
API_ARBITRUM_GETLOGS = (
    "https://api.arbiscan.io/api?module=logs&action=getLogs&fromBlock=%s&toBlock=%s&address=%s&topic0=%s&apikey=%s"
)
API_ROPSTEN_GETLOGS = "https://api-ropsten.etherscan.io/api?module=logs&action=getLogs&fromBlock=%s&toBlock=%s&address=%s&topic0=%s&apikey=%s"
API_KOVAN_GETLOGS = "https://api-kovan.etherscan.io/api?module=logs&action=getLogs&fromBlock=%s&toBlock=%s&address=%s&topic0=%s&apikey=%s"
API_GOERLI_GETLOGS = "https://api-goerli.etherscan.io/api?module=logs&action=getLogs&fromBlock=%s&toBlock=%s&address=%s&topic0=%s&apikey=%s"

# TOKEN INFO
API_ETHERSCAN_GETTOKENINFO = "https://api.etherscan.io/api?module=token&action=tokeninfo&contractaddress=%s&apikey=%s"
API_ETHPLORER_GETTOKENINFO = "https://api.ethplorer.io/getTokenInfo/%s?apiKey=%s"
API_BLOCKSCOUT_GETTOKENCONTRACT = (
    "https://blockscout.com/xdai/mainnet/api?module=token&action=getToken&contractaddress=%s"
)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# IMPLEMENTATION SLOTS for OpenZeppelins' EIPs
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
IMPLEMENTATION_SLOT_EIP_1967 = "0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc"
IMPLEMENTATION_SLOT_UNSTRUCTURED = "0x7050c9e0f4ca769c69bd3a8ef740bc37934f8e2c036e5a723fd8ee048ed3f8c3"
