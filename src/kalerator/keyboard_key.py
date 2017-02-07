# coding=UTF-8
from decimal import Decimal

from .config import key_spacing_in, key_spacing_mm
from .diode import Diode
from .functions import float_to_str, translate_board_coords


class KeyboardKey(object):
    """Abstraction for keyboard switches.
    """
    def __init__(self, name, left_key, next_key, eagle_version, coord, coord_mm, offset, switch_footprint, diode):
        self.name = name.replace(' ', '')
        self.left_key = left_key
        self.coord = coord[:]
        self._coord_mm = coord_mm[:]
        self.eagle_version = eagle_version
        self.switch_footprint = switch_footprint
        self._board_scr = None
        self._schematic_scr = None
        self.width = next_key['w']
        self.diode = Diode(self.name, self.coord_in, self.coord_mm, **diode)
        self.column_pin_scr = (
            self.coord_in[0] - Decimal('0.3'),
            self.coord_in[1] + Decimal('0.1'),
        )
        self.row_pin = (
            self.coord_mm[0] - Decimal('8.75'),
            self.coord_mm[1] + Decimal('3'),
        )
        self.column_header_pin = (
            self.coord_mm[0] + Decimal('3.35'),
            self.coord_mm[1] - Decimal('9.55'),
        )
        self.row_header_pin = (
            self.coord_mm[0] - Decimal('8.93'),
            self.coord_mm[1] + Decimal('4.88'),
        )

        # Figure out where our pins are
        self.sch_pin = [self.coord_in[0] - Decimal('0.1'), self.coord_in[1] + Decimal('0.7')]

    @property
    def board_scr(self):
        if not self._board_scr:
            self._generate_board()

        return self._board_scr

    @property
    def schematic_scr(self):
        if not self._schematic_scr:
            self._generate_schematic()

        return '\n'.join(self._schematic_scr)

    @property
    def coord_in(self):
        # Kludge: footprint is long
        return (self._coord_mm[0] * Decimal('0.0393701'),
                (self._coord_mm[1] * Decimal('0.0393701')) * 2)

    @property
    def coord_mm(self):
        coords = [self._coord_mm[0], self._coord_mm[1]]

        if self.width > 1:  # What's this for? I don't remember. :(
            extra_width = (self.width - 1) * key_spacing_mm
            offset_amount = extra_width / 2
            coords[0] += offset_amount

        return coords

    def _generate_board(self):
        """Create the script snippet for this key's piece of the board.
        """
        board_scr = [
            'ROTATE R180 %s;' % self.name,
            'MOVE %s (%s %s);' % (
                self.name,
                float_to_str(self.coord_mm[0]),
                float_to_str(self.coord_mm[1])
            ),
            self.diode.board_scr
        ]

        self._board_scr = '\n'.join(board_scr)

        if self.eagle_version == 'free':
            self._board_scr = translate_board_coords(self._board_scr)

    def _generate_schematic(self):
        """Create the script snippet for this key's piece of the schematic.
        """
        self._schematic_scr = [
            'ADD %s %s (%s %s);' % (
                self.switch_footprint,
                self.name,
                float_to_str(self.coord_in[0]),
                float_to_str(self.coord_in[1])
            ),
            self.diode.schematic_scr
        ]

        if self.left_key:
            if self.left_key.sch_pin[1] == self.sch_pin[1]:
                self._schematic_scr.append('NET ROW%s (%s %s) (%s %s);' % (
                    self.coord[1] + 1,
                    float_to_str(self.left_key.sch_pin[0]),
                    float_to_str(self.left_key.sch_pin[1]),
                    float_to_str(self.sch_pin[0]),
                    float_to_str(self.sch_pin[1])
                ))
