# coding=UTF-8
import re


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


def translate_board_coords(board_scr):
    """Translate coordinates into the upper-right quadrant.

    Returns a copy of board_scr with all coordinates shifted to fit into the
    free version of EAGLE.
    """
    offset = -8.8, 112.8
    full_coord_re = re.compile(r"\(-?\d+\.?\d* -?\d+\.?\d*\)")
    coord_re = re.compile(r"\((-?\d+\.?\d*) (-?\d+\.?\d*)\)")

    skeleton_scr = full_coord_re.sub('%s', board_scr)
    matches = []

    for match in full_coord_re.finditer(board_scr):
        if match:
            coords = match.group()
            if coords:
                coords = coord_re.match(coords)
                coords = map(float, coords.groups())
                coords[0] = coords[0] + offset[0]
                coords[1] = coords[1] + offset[1]

                matches.append('(%s %s)' % (
                    float_to_str(coords[0]), float_to_str(coords[1])
                ))

    return skeleton_scr % tuple(matches)
