from defabipedia import Chain

from defyes.porfolio import ERC20Token, TokenAmount, UnderlyingTokenAmount, Unwrappable


class VaultToken(Unwrappable, ERC20Token):
    pass


class tokens:
    class ethereum:
        class _aurawstETH_WETH_BPT_vault(VaultToken):
            chain = Chain.ETHEREUM
            address = "0x2a14dB8D09dB0542f6A371c0cB308A768227D67D"

            def unwrap(self, tokenamount: TokenAmount) -> UnderlyingTokenAmount:
                from defyes.protocols.balancer import newarch as balancer

                utoken = balancer.tokens.ethereum.wstETH_WETH_BPT
                return UnderlyingTokenAmount(token=utoken, amount_teu=tokenamount.amount_teu)

        aurawstETH_WETH_BPT_vault = _aurawstETH_WETH_BPT_vault()
