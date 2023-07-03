import pytest

from defyes.constants import ETHEREUM, XDAI
from defyes.util.api import RequestFromScan

ADDRESS_N1 = "0x458cD345B4C05e8DF39d0A07220feb4Ec19F5e6f"
ABI_N1 = '{"internalType":"bytes","name":"signatures","type":"bytes"}],"name":"execTransaction","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"payable","type":"function"}'
ADDRESS_N2 = "0xbf65bfcb5da067446CeE6A706ba3Fe2fB1a9fdFd"
ABI_N2 = '{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}'
ADDRESS_N3 = "0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83"
ABI_N3 = '{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}'
ADDRESS_N4 = "0xD6A6372e371AF57c773176C41DD4a26f6084b37E"
ABI_N4 = "Contract source code not verified"

test_cases = [
    (XDAI, "contract", "getabi", {"address": ADDRESS_N1}, ABI_N1),
    (XDAI, "contract", "getabi", {"address": ADDRESS_N2}, ABI_N2),
    (XDAI, "contract", "getabi", {"address": ADDRESS_N3}, ABI_N3),
    (XDAI, "contract", "getabi", {"address": ADDRESS_N4}, ABI_N4),
    (ETHEREUM, "block", "getblockreward", {"blockno": 2165403}, "blockReward"),
]


@pytest.mark.parametrize("blockchain,module,action,kwargs,expected_data", test_cases)
def test_request(blockchain, module, action, kwargs, expected_data):
    data = RequestFromScan(blockchain=blockchain, module=module, action=action, kwargs=kwargs).request()["result"]
    assert expected_data in data
