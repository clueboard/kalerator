# coding=UTF-8
def float_to_str(num):
    """Converts a float to a string that never has more than 2 decimal places.

    :param num: int
    :return: str
    """
    num_str = '%f' % num
    integer, fp = num_str.split('.', 1)
    fp = fp[:2]

    return '.'.join((integer, fp))


def to_imperial(mm):
    """Converts mm to in.

    :param mm: int
    :return: int
    """
    return mm / 25.4
