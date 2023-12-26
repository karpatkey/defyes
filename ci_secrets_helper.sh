JQ="      .nodes.ethereum.latest   = [\"${NODE_ETH}\"]"
JQ=$JQ" | .nodes.ethereum.archival = [\"${NODE_ETH}\"]"
JQ=$JQ" | .nodes.gnosis.archival   = [\"${NODE_XDAI}\"]"
JQ=$JQ" | .nodes.polygon.archival  = [\"${NODE_POLYGON}\"]"
JQ=$JQ" | .nodes.optimism.archival = [\"${NODE_OPTIMISM}\"]"
JQ=$JQ" | .nodes.arbitrum.archival = [\"${NODE_ARBITRUM}\"]"
JQ=$JQ" | .apikeys.etherscan       = \"${APIKEYS_ETHERSCAN}\""
JQ=$JQ" | .apikeys.polscan         = \"${APIKEYS_POLSCAN}\""
JQ=$JQ" | .apikeys.gnosisscan      = \"${APIKEYS_GNOSISSCAN}\""
JQ=$JQ" | .apikeys.optimisticetherscan = \"${APIKEYS_OPTIMISM}\""
JQ=$JQ" | .apikeys.arbiscan        = \"${APIKEYS_ARBITRUM}\""
echo $JQ 

jq "$JQ" < defyes/config.json > /tmp/tmp_config.json
