import logging
from .config import diode, switches
from .functions import float_to_str
from .keyboard_key import KeyboardKey


class Keyboard(dict):
    def __init__(self, rawdata):
        """Representation of a keyboard.

        :param rawdata: Keyboard object from keyboard-layout-editor.com
        """
        super(Keyboard, self).__init__()
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
        """Generate and return the script snippets for keys and their rows.
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
                        key_name += '_DUPE'

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
