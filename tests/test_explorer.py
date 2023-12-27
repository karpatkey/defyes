import pytest
from web3 import Web3

from defyes.constants import Chain
from defyes.explorer import ChainExplorer

ADDRESS_N1 = "0x458cD345B4C05e8DF39d0A07220feb4Ec19F5e6f"
ABI_N1 = '{"internalType":"bytes","name":"signatures","type":"bytes"}],"name":"execTransaction","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"payable","type":"function"}'
ADDRESS_N2 = "0xbf65bfcb5da067446CeE6A706ba3Fe2fB1a9fdFd"
ABI_N2 = '{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}'
ADDRESS_N3 = "0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83"
ABI_N3 = '{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}'
ADDRESS_N4 = "0xD6A6372e371AF57c773176C41DD4a26f6084b37E"


def test_avalanche_time_from_block():
    time = ChainExplorer(Chain.AVALANCHE).time_from_block(39_455_385)
    assert time == 1_703_419_194


test_cases = [
    (Chain.GNOSIS, ADDRESS_N1, ABI_N1),
    (Chain.GNOSIS, ADDRESS_N2, ABI_N2),
    (Chain.GNOSIS, ADDRESS_N3, ABI_N3),
]


@pytest.mark.parametrize("blockchain,address,partial_abi", test_cases)
def test_get_abi(blockchain, address, partial_abi):
    abi = ChainExplorer(blockchain).abi_from_address(address)
    assert partial_abi in abi


def test_get_abi_fail():
    with pytest.raises(Exception) as exc_info:
        ChainExplorer(Chain.GNOSIS).abi_from_address(ADDRESS_N4)

    assert exc_info.value.args[0] == "ABI not verified."


def test_contract_creation():
    contract = ChainExplorer(Chain.ETHEREUM).get_contract_creation("0x6B175474E89094C44Da98b954EedeAC495271d0F")
    assert contract == [
        {
            "contractAddress": "0x6b175474e89094c44da98b954eedeac495271d0f",
            "contractCreator": "0xddb108893104de4e1c6d0e47c42237db4e617acc",
            "txHash": "0x495402df7d45fe36329b0bd94487f49baee62026d50f654600f6771bd2a596ab",
        }
    ]


def test_get_logs():
    blockstart = 16671522
    blockend = 16671547
    vault_address = 0xBA12222222228D8BA445958A75A0704D566BF2C8

    swap_event = Web3.keccak(text="Swap(bytes32,address,address,uint256,uint256)").hex()
    pool_id = "0x5c6ee304399dbdb9c8ef030ab642b10820db8f56000200000000000000000014"

    logs = ChainExplorer(Chain.ETHEREUM).get_logs(
        vault_address, blockstart, blockend, swap_event, optional_params={"topic1": pool_id}
    )
    assert logs == [
        {
            "address": "0xba12222222228d8ba445958a75a0704d566bf2c8",
            "topics": [
                "0x2170c741c41531aec20e7c107c24eecfdd15e69c9bb0a8dd37b1840b9e0b207b",
                "0x5c6ee304399dbdb9c8ef030ab642b10820db8f56000200000000000000000014",
                "0x000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
                "0x000000000000000000000000ba100000625a3754423978a60c9317c58a424e3d",
            ],
            "data": "0x0000000000000000000000000000000000000000000000007d24b6d0c338c40000000000000000000000000000000000000000000000006ec9dbd910381f2302",
            "blockNumber": "0xfe6328",
            "blockHash": "0xd1495a48d4054e5706ebdbb6b1413b95124605b02362f11a5ada1aef183f88d5",
            "timeStamp": "0x63f3bb43",
            "gasPrice": "0x8df66421d",
            "gasUsed": "0x1d8b1",
            "logIndex": "0xfd",
            "transactionHash": "0x0abba9d11ffb45d52d2ed95ebe8307d029c392b7972f86eec1acdac851925f44",
            "transactionIndex": "0x65",
        },
        {
            "address": "0xba12222222228d8ba445958a75a0704d566bf2c8",
            "topics": [
                "0x2170c741c41531aec20e7c107c24eecfdd15e69c9bb0a8dd37b1840b9e0b207b",
                "0x5c6ee304399dbdb9c8ef030ab642b10820db8f56000200000000000000000014",
                "0x000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
                "0x000000000000000000000000ba100000625a3754423978a60c9317c58a424e3d",
            ],
            "data": "0x0000000000000000000000000000000000000000000000006e6088ec0a459400000000000000000000000000000000000000000000000061aea368d094c6a871",
            "blockNumber": "0xfe6336",
            "blockHash": "0xbb53a31224bfc8cee037b4cd7dbdacec21d7975aa1818863f42eb7e63cfadcf5",
            "timeStamp": "0x63f3bbeb",
            "gasPrice": "0x7c0ee6a91",
            "gasUsed": "0x1ed88",
            "logIndex": "0x1f8",
            "transactionHash": "0xcc8611b7f26417573fce89fef95bde54fed87ce716dffa5fea2b13ed190a83bc",
            "transactionIndex": "0xd0",
        },
    ]
