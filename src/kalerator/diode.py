# coding=UTF-8
from .config import trace_width
from .keyboard import float_to_str


class Diode(object):
    """Abstraction for keyboard diodes.
    """
    def __init__(self, name, coord_in, coord_mm, footprint,
                 switch_offset_board, switch_offset_schematic,
                 switch_pin_offset, pin_neg_offset, pin_pos_offset):
        self.name = name
        self.footprint = footprint
        self.coord_in = (coord_in[0] + switch_offset_schematic[0],
                         coord_in[1] + switch_offset_schematic[1])
        self.coord_mm = (coord_mm[0] + switch_offset_board[0],
                         coord_mm[1] + switch_offset_board[1])
        self.switch_pin = (coord_mm[0] + switch_pin_offset[0],
                           coord_mm[1] + switch_pin_offset[1])
        self.pin_neg = (self.coord_mm[0] + pin_neg_offset[0],
                        self.coord_mm[1] + pin_neg_offset[1])
        self.pin_pos = (self.coord_mm[0] + pin_pos_offset[0],
                        self.coord_mm[1] + pin_pos_offset[1])

    @property
    def board_scr(self):
        """Returns the script snippets for moving the diode into place.
        """
        return '\n'.join((
            'ROTATE R90 D%s;' % self.name,
            'MOVE D%s (%s %s);' % (
                self.name,
                float_to_str(self.coord_mm[0]),
                float_to_str(self.coord_mm[1])
            ),
            'WIRE 16 %s (%s %s) (%s %s);' % (
                trace_width,
                self.pin_neg[0],
                self.pin_pos[1],
                float_to_str(self.switch_pin[0]),
                float_to_str(self.switch_pin[1])
            )
        ))

    @property
    def schematic_scr(self):
        return 'ADD %s D%s R90 (%s %s);' % (
            self.footprint,
            self.name,
            float_to_str(self.coord_in[0]),
            float_to_str(self.coord_in[1]),
        )
