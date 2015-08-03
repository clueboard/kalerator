from kalerator.functions import float_to_str, to_imperial


def test_float_to_str():
    assert float_to_str(2.0000000000000000005) == '2.00'

def test_to_imperial():
    assert to_imperial(100) == 3.937007874015748

