from defyes.portfolio import Asset


def test_hash():
    for asset in Asset.instances:
        hash(asset)
