JQ="      .nodes.ethereum   = [\"${NODE_ETH}\"]"
JQ=$JQ" | .nodes.gnosis   = [\"${NODE_XDAI}\"]"
JQ=$JQ" | .nodes.polygon  = [\"${NODE_POLYGON}\"]"
JQ=$JQ" | .nodes.optimism = [\"${NODE_OPTIMISM}\"]"
JQ=$JQ" | .nodes.arbitrum = [\"${NODE_ARBITRUM}\"]"
JQ=$JQ" | .nodes.avalanche = [\"${NODE_AVALANCHE}\"]"
JQ=$JQ" | .nodes.base = [\"${NODE_BASE}\"]"
JQ=$JQ" | .nodes.metis = [\"${NODE_METIS}\"]"
JQ=$JQ" | .apikeys.etherscan       = \"${APIKEYS_ETHERSCAN}\""
JQ=$JQ" | .apikeys.polscan         = \"${APIKEYS_POLSCAN}\""
JQ=$JQ" | .apikeys.gnosisscan      = \"${APIKEYS_GNOSISSCAN}\""
JQ=$JQ" | .apikeys.optimisticetherscan = \"${APIKEYS_OPTIMISM}\""
JQ=$JQ" | .apikeys.arbiscan        = \"${APIKEYS_ARBITRUM}\""
JQ=$JQ" | .apikeys.metisexplorer   = \"${APIKEYS_METISEXPLORER}\""
JQ=$JQ" | .apikeys.basescan        = \"${APIKEYS_BASESCAN}\""
JQ=$JQ" | .apikeys.snowtrace       = \"${APIKEYS_SNOWTRACE}\""
echo $JQ 

jq "$JQ" < example_config.json > /tmp/tmp_config.json
