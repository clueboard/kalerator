import logging


key_spacing_mm = 19.05
key_spacing_in = 0.75
trace_width = 0.5  # MM
diode = {
    'footprint': "DIODE'1N4148'@Seeed-OPL-Diode",
    'switch_offset_board': (-8.95, 0),
    'switch_offset_schematic': (-0.1, 0.45),
    'switch_pin_offset': (-2.54, -5.08),
    'pin_neg_offset': (0, 3),
    'pin_pos_offset': (0, -3),
}
switches = {
    # If the switch width doesn't match any key in this dictionary,
    # that switch gets the 'DEFAULT' component.
    'DEFAULT': 'ALPSMX-1U-LED@AlpsCherry',
    2: 'ALPSMX-2U-LED@AlpsCherry',
    2.25: 'ALPSMX-2U-LED@AlpsCherry',
    2.5: 'ALPSMX-2U-LED@AlpsCherry',
    2.75: 'ALPSMX-2U-LED@AlpsCherry',
}


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
        self.sch_pin_neg = (0, 0)  # FIXME
        self.sch_pin_pos = (0, 0)  # FIXME

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


class KeyboardKey(object):
    """Abstraction for keyboard switches.
    """
    def __init__(self, name, left_key, next_key, coord, offset,
                 footprint=switches['DEFAULT'], diode=diode):
        self.name = name.replace(' ', '')
        self.left_key = left_key
        self.coord = coord[:]
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

        # Figure out where our pins are
        self.sch_pin = [self.coord_in[0] - 0.1, self.coord_in[1] + 0.6]

    @property
    def board_scr(self):
        if not self._board_scr:
            self._generate_board()

        return '\n'.join(self._board_scr)

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
        self._board_scr = [
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
                self._board_scr.append('ROUTE %s (%s %s) (%s %s);' % (
                    trace_width,
                    float_to_str(self.left_key.row_pin[0] + 0.01),
                    float_to_str(self.left_key.row_pin[1]),
                    float_to_str(self.row_pin[0] - 0.01),
                    float_to_str(self.row_pin[1])
                ))

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
                    self.coord_in[1] * -1,
                    float_to_str(self.left_key.sch_pin[0]),
                    float_to_str(self.left_key.sch_pin[1]),
                    float_to_str(self.sch_pin[0]),
                    float_to_str(self.sch_pin[1])
                ))

            else:
                logging.warn(
                    'Attempting to create invalid ROW net: '
                    'LastKey:%s Key:%s LastKeyPin:%s KeyPin:%s',
                    self.left_key.name, self.name,
                    self.left_key.sch_pin, self.sch_pin
                )


class Kalerator(dict):
    def __init__(self, rawdata):
        """
        :param rawdata:
            JSON text from keyboard-layout-editor.com
        """
        super(Kalerator, self).__init__()
        self.rawdata = rawdata
        self.rows = []
        self.max_col = 0
        self.schematic_preamble = '\n'.join(('GRID ON;',
                                             'GRID IN 0.1 1;',
                                             'GRID ALT IN 0.01;',
                                             'SET WIRE_BEND 2;',
                                             '',
                                             ''))
        self.schematic_footer = '\n\nWINDOW FIT;'
        self.board_preamble = '\n'.join(('GRID ON;',
                                         'GRID MM 1 10;',
                                         'GRID ALT MM .1;',
                                         '',
                                         ''))
        self.board_footer = '\n\nRATSNEST;\nWINDOW FIT;'
        self.default_next_key = {
            'y': 0,
            'w': 1,
            'h': 1,
        }
        self.sch_col_offset = (-0.3, 0.1)  # IN
        self.parse_json()

    def __iter__(self):
        """Overload iteration so we can iterate over the keys in order.
        """
        for row in self.rows:
            for key in row:
                yield key

    @property
    def key_scr(self):
        """Generate and return the script snippets for keys and their rows
        """
        board_scr = []
        schematic_scr = []

        for row in self.rows:
            for key in row:
                board_scr.append(key.board_scr)
                schematic_scr.append(key.schematic_scr)

        return '\n'.join(schematic_scr), '\n'.join(board_scr)

    @property
    def column_scr(self):
        """Generate and return the script snippets for connecting columns.
        """
        schematic_scr = []

        for column in range(1, self.max_col):
            key = last_key = None

            for row in self.rows:
                try:
                    # Grab columns from alternating sides so that we don't end
                    # up with weird traces for things like the spacebar.
                    if column % 2 == 0:
                        key = row.pop(0)
                    else:
                        key = row.pop(-1)
                except IndexError:
                    last_key = key
                    continue

                if last_key:
                    top_pin_offset = last_key.column_pin_scr[1] - 0.5
                    bot_pin_offset = key.column_pin_scr[1] + 0.75

                    # We use 3 NET's here to ensure that the column won't
                    # intersect another switch and cause confusion.
                    schematic_scr.append('NET COLUMN%s (%s %s) (%s %s);' % (
                        column,
                        float_to_str(last_key.column_pin_scr[0]),
                        float_to_str(last_key.column_pin_scr[1]),
                        float_to_str(last_key.column_pin_scr[0]),
                        float_to_str(top_pin_offset)
                    ))
                    schematic_scr.append('NET COLUMN%s (%s %s) (%s %s);' % (
                        column,
                        float_to_str(last_key.column_pin_scr[0]),
                        float_to_str(top_pin_offset),
                        float_to_str(key.column_pin_scr[0]),
                        float_to_str(bot_pin_offset)
                    ))
                    schematic_scr.append('NET COLUMN%s (%s %s) (%s %s);' % (
                        column,
                        float_to_str(key.column_pin_scr[0]),
                        float_to_str(bot_pin_offset),
                        float_to_str(key.column_pin_scr[0]),
                        float_to_str(key.column_pin_scr[1])
                    ))

                last_key = key

        return '\n'.join(schematic_scr)

    def generate(self):
        """Generate and return the Schematic and Board scripts.
        """
        schematic_key_scr, board_key_scr = self.key_scr
        schematic_scr = [self.schematic_preamble, schematic_key_scr,
                         self.column_scr, self.schematic_footer]
        board_scr = [self.board_preamble, board_key_scr, self.board_footer]

        return schematic_scr, board_scr

    def parse_json(self):
        """Parse the KLE JSON into a data structure we can iterate over.
        """
        # Initialize the state engine we use to parse K-L-E's data format
        last_key = None
        next_key = self.default_next_key.copy()
        col_num = 0
        current_attrs = {
            'coord': [0, 0],
            'offset': [0, 0],
        }

        for row in self.rawdata:
            if isinstance(row, dict):
                logging.warn('Not reading keyboard properties: %s' % row)
                continue

            if not isinstance(row, list):
                logging.warn("Don't know how to deal with this row: %s", row)
                continue

            self.rows.append([])

            # Modify our state engine for the new row
            current_attrs['coord'][0] = 1
            current_attrs['coord'][1] += 1
            current_attrs['offset'] = [0, 0]

            for item in row:
                if isinstance(item, (str, unicode)):
                    col_num += 1
                    # Prototype our key
                    key_name = item.split('\n', 1)[0].upper()

                    if key_name == '':
                        logging.warn("Blank key name! Assuming it's SPACE.")
                        key_name = 'SPACE'

                    if key_name in self:
                        logging.warn('Duplicate key %s! Renaming to %s_DUPE!',
                                     key_name, key_name)
                        key_name = key_name + '_DUPE'

                    footprint = switches[next_key['w']] \
                        if next_key['w'] in switches else \
                        switches['DEFAULT']

                    self.rows[-1].append(None)  # Ugly hack
                    self[key_name] = self.rows[-1][-1] = \
                        KeyboardKey(key_name, last_key, next_key,
                                    footprint=footprint, diode=diode,
                                    **current_attrs)

                    # Prepare for the next key we'll have to process
                    current_attrs['coord'][0] += next_key['w']
                    last_key = self[key_name]
                    next_key = self.default_next_key.copy()

                elif isinstance(item, dict):
                    # Change attributes about the next key
                    for attribute, value in item.items():
                        if attribute == 'x':
                            current_attrs['coord'][0] += value

                        elif attribute in ['y', 'w', 'h', 'l', 'n']:
                            next_key[attribute] = value

                        else:
                            logging.debug('Unknown next_key attribute: '
                                          '%s (Value: %s)', attribute, value)

                else:
                    logging.error('Unknown key or object: %s', item)

            # Store this column count if it's the highest we've seen
            if col_num > self.max_col:
                self.max_col = col_num

            col_num = 0
