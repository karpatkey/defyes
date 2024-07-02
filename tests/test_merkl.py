import json
from decimal import Decimal
from unittest.mock import Mock, patch

from defyes.protocols.merkl import get_protocol_data_for


@patch("requests.get")
def test_get_protocol_data_for(mock_get):
    # Arrange
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = json.dumps(
        {"1": {"transactionData": {"0x40D16FC0246aD3160Ccc09B8D0D3A2cD28aE6C2f": {"claim": "23554502914860344301100"}}}}
    )
    mock_get.return_value = mock_response

    # Act
    result = get_protocol_data_for("ethereum", "0x849D52316331967b6fF1198e5E32A0eB168D039d")

    # Assert
    expected_result = {
        "blockchain": "ethereum",
        "block": 19975671,
        "protocol": "Merkl",
        "positions_key": None,
        "version": 0,
        "wallet": "0x849D52316331967b6fF1198e5E32A0eB168D039d",
        "decimals": "",
        "positions": {
            "rewards": [
                {
                    "address": "0x40D16FC0246aD3160Ccc09B8D0D3A2cD28aE6C2f",
                    "balance": Decimal("23554.5029148603443011"),
                }
            ]
        },
    }

    assert result["blockchain"] == expected_result["blockchain"]
    assert "block" in result and isinstance(result["block"], int)
    assert result["protocol"] == expected_result["protocol"]
    assert result["positions_key"] == expected_result["positions_key"]
    assert result["version"] == expected_result["version"]
    assert result["wallet"] == expected_result["wallet"]
    assert result["decimals"] == expected_result["decimals"]
    assert result["positions"] == expected_result["positions"]
