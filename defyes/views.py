from collections import defaultdict

from defyes.portfolio import Portfolio, TokenPosition


def like_debank(portfolio: Portfolio, show_fiat=False):
    inprotocol, inwallet = boolsplit(portfolio.token_positions, lambda pos: pos.underlying)
    print("Wallet")
    for pos in inwallet:
        print_amounts(pos, "  ")
        if pos and show_fiat:
            print(f"    {pos.amount_fiat!r}")
    print()

    for protocol, positions in groupby(inprotocol + portfolio.positions, lambda pos: pos.protocol).items():
        print(protocol)
        print_pos(portfolio, positions, show_fiat=show_fiat)
        print()


def print_amounts(pos, prefix=""):
    print(f"{prefix}{pos.token.symbol} {decimal_format(pos.amount)}")


def decimal_format(dec):
    s = str(dec)
    if "." in s:
        inte, frac = s.split(".")
        return f"{format(int(inte), '_')}.{frac}"
    else:
        return s


def print_pos(portfolio, positions, level=1, show_fiat=False):
    for pos in positions:
        if isinstance(pos, TokenPosition):
            print_amounts(pos, "  " * level)
            if pos and show_fiat and not pos.underlying:
                print(f"{'  '*(level+1)}{pos.amount_fiat!r}")
            if pos.token in portfolio.target_tokens:
                continue
        else:
            print(f"  {pos.__class__.__name__}")
        if pos.underlying:
            print_pos(portfolio, pos.underlying, level + 1, show_fiat)


def boolsplit(seq, key=lambda element: element):
    true, false = [], []
    for element in seq:
        (true if key(element) else false).append(element)
    return true, false


def groupby(seq, key):
    d = defaultdict(list)
    for element in seq:
        d[key(element)].append(element)
    return dict(d)
