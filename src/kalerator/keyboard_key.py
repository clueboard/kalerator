# coding=UTF-8
from .config import diode, key_spacing_in, key_spacing_mm, switches, \
    trace_width
from .diode import Diode
from .functions import float_to_str, translate_board_coords


class KeyboardKey(object):
    """Abstraction for keyboard switches.
    """
    def __init__(self, name, left_key, next_key, eagle_version, coord, offset,
                 footprint=switches['DEFAULT'], diode=diode):
        self.name = name.replace(' ', '')
        self.left_key = left_key
        self.coord = coord[:]
        self.eagle_version = eagle_version
        self.footprint = footprint
        self._board_scr = None
        self._schematic_scr = None
        self.width = next_key['w']
        self.coord[1] += next_key['y']
        self.coord[1] *= -1  # Inverted because K-L-E has an upside-down Y axis
        self.diode = Diode(self.name, self.coord_in, self.coord_mm, **diode)
        self.column_pin_scr = (
            self.coord_in[0] - 0.3,
            self.coord_in[1] + 0.1,
        )
        self.row_pin = (
            self.coord_mm[0] - 8.75,
            self.coord_mm[1] + 3,
        )
        self.column_header_pin = (
            self.coord_mm[0] + 3.35,
            self.coord_mm[1] - 9.55,
        )
        self.row_header_pin = (
            self.coord_mm[0] - 8.93,
            self.coord_mm[1] + 4.88,
        )

        # Figure out where our pins are
        self.sch_pin = [self.coord_in[0] - 0.1, self.coord_in[1] + 0.6]

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
        return (self.coord[0] * key_spacing_in,
                (self.coord[1] * key_spacing_in) * 2)

    @property
    def coord_mm(self):
        coords = [self.coord[0] * key_spacing_mm,
                  self.coord[1] * key_spacing_mm]

        if self.width > 1:
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

        if self.left_key:
            if self.left_key.row_pin[1] == self.row_pin[1]:
                board_scr.append('ROUTE %s (%s %s) (%s %s);' % (
                    trace_width,
                    float_to_str(self.left_key.row_pin[0] + 0.01),
                    float_to_str(self.left_key.row_pin[1]),
                    float_to_str(self.row_pin[0] - 0.01),
                    float_to_str(self.row_pin[1])
                ))

        else:
            board_scr.append(
                'MOVE PROW%s (%s %s);' % (
                    self.coord[1] * -1,
                    self.row_header_pin[0],
                    self.row_header_pin[1]
                )
            )

        self._board_scr = '\n'.join(board_scr)

        if self.eagle_version == 'free':
            self._board_scr = translate_board_coords(self._board_scr)

    def _generate_schematic(self):
        """Create the script snippet for this key's piece of the schematic.
        """
        self._schematic_scr = [
            'ADD %s %s (%s %s);' % (
                self.footprint,
                self.name,
                float_to_str(self.coord_in[0]),
                float_to_str(self.coord_in[1])
            ),
            self.diode.schematic_scr
        ]

        if self.left_key:
            if self.left_key.sch_pin[1] == self.sch_pin[1]:
                self._schematic_scr.append('NET ROW%s (%s %s) (%s %s);' % (
                    self.coord[1] * -1,
                    float_to_str(self.left_key.sch_pin[0]),
                    float_to_str(self.left_key.sch_pin[1]),
                    float_to_str(self.sch_pin[0]),
                    float_to_str(self.sch_pin[1])
                ))

        else:
            self._schematic_scr.append(
                'ADD HEADER-1P-KEYBOARD@Headers PROW%s R90 (%s %s);\n' % (
                    self.coord[1] * -1,
                    self.sch_pin[0],
                    self.sch_pin[1]
                ) + 'JUNCTION (%s %s);\n' % (
                    self.sch_pin[0],
                    self.sch_pin[1]
                ) + 'NAME ROW%s (%s %s);\n' % (
                    self.coord[1] * -1,
                    self.sch_pin[0],
                    self.sch_pin[1]
                )
            )
