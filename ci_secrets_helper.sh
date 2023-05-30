JQ="      .nodes.ethereum.latest   = [\"${NODE_ETH}\"]"
JQ=$JQ" | .nodes.ethereum.archival = [\"${NODE_ETH}\"]"
JQ=$JQ" | .nodes.xdai.archival     = [\"${NODE_XDAI}\"]"
JQ=$JQ" | .nodes.polygon.archival  = [\"${NODE_POLYGON}\"]"
JQ=$JQ" | .nodes.optimism.archival = [\"${NODE_OPTIMISM}\"]"
JQ=$JQ" | .apikeys.etherscan       = \"${APIKEYS_ETHERSCAN}\""
JQ=$JQ" | .apikeys.polscan         = \"${APIKEYS_POLSCAN}\""
echo $JQ 

jq "$JQ" < defi_protocols/config.json > /tmp/tmp_config.json
