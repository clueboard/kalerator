from copy import deepcopy
import json
import logging


__author__ = 'skully'


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


class Kalerator(object):
    def __init__(self, kle_json):
        """
        :param kle_json:
            JSON text from keyboard-layout-editor.com
        """
        # The components we'll use for this board. Can be overridden after this
        # object is instaniated to tweak behavior.
        self.diode = "DIODE'1N4148'@Seeed-OPL-Diode"
        self.switches = {
            # To support other switch widths. The key is the width as reported
            # by K-L-E and the value is the footprint to use instead of
            # self.switch. Any key that doesn't match a width here gets
            # 'DEFAULT'.
            'DEFAULT': 'ALPSMX-1U-LED@AlpsCherry',
            '2': 'ALPSMX-2U-LED@AlpsCherry',
            '2.25': 'ALPSMX-2U-LED@AlpsCherry',
            '2.5': 'ALPSMX-2U-LED@AlpsCherry',
        }

        # How wide to make the copper traces between switches
        self.trace_width = 0.5  # MM

        # Set the schematic to the "no bend" WIRE_BEND mode
        self.schematic_preamble = 'SET WIRE_BEND 2;\n\n'

        # For the board layout set the grid to 1MM
        self.layout_preamble = 'GRID ON;\nGRID MM 1 10;\nGRID ALT MM .1;\n\n'

        # Conversion factors
        self.sch_diode_offset = (-0.1, 0.45)    # IN
        self.sch_net_offset = (-0.1, 0.6)       # IN
        self.sch_col_offset = (-0.3, 0.1)       # IN
        self.key_spacing = 19.05                # MM
        self.layout_diode_offset = (-8.75, -7)  # MM
        self.layout_sw_pin_0 = (-2.54, -5.08)   # MM
        self.layout_diode_neg = (-8.75, -4)     # MM
        self.layout_diode_pos = (-8.75, -10)    # MM

        # Some state tracking objects
        self.rawdata = json.loads(kle_json)
        self.keys = None
        self.default_next_key = {
            'y': 0,
            'w': 1,
            'h': 1,
        }

    def generate(self):
        """Generate the Schematic and Board scripts.

        :return: (schematic_scr, board_scr)
        """
        if not self.keys:
            self.parse_json()

        col_num = 0
        row_num = 0
        maxcol = 0
        last_key_pos = None
        board_scr = [self.layout_preamble]
        schematic_scr = [self.schematic_preamble]

        for row in self.keys:
            for key in row:
                col_num += 1
                for axis in 0, 1:
                    # Map keyboard units to MM
                    key['coord'][axis] *= self.key_spacing

                    # If this key is offset we need to adjust the center
                    if key['offset'][axis]:
                        offset_mm = key['offset'][axis] * (self.key_spacing/2)
                        key['coord'][axis] += offset_mm

                # Position this switch/diode on the schematic
                switch_position = (
                    to_imperial(key['coord'][0]),
                    to_imperial(key['coord'][1]) * 2
                )
                diode_position = [switch_position[i] + self.sch_diode_offset[i]
                                  for i in range(2)]
                device_name = str(key['width'])

                if device_name in self.switches:
                    device_name = self.switches[device_name]
                else:
                    device_name = self.switches['DEFAULT']

                schematic_scr.append('ADD %s %s (%s %s);' % (
                    device_name,
                    key['label'],
                    float_to_str(switch_position[0]),
                    float_to_str(switch_position[1])
                ))
                schematic_scr.append('ADD %s D%s R90 (%s %s);' % (
                    self.diode,
                    key['label'],
                    float_to_str(diode_position[0]),
                    float_to_str(diode_position[1])
                ))
                schematic_scr.append('VALUE D%s 1N4148;' % (key['label']))

                # Position this switch/diode on the board
                diode_pos = [key['coord'][i] + self.layout_diode_offset[i]
                             for i in range(2)]
                diode_neg_pos = [key['coord'][i] + self.layout_diode_neg[i]
                                 for i in range(2)]
                diode_pos_pos = [key['coord'][i] + self.layout_diode_pos[i]
                                 for i in range(2)]
                sw_pin_0_pos = [key['coord'][i] + self.layout_sw_pin_0[i]
                                for i in range(2)]

                board_scr.append('ROTATE R180 %s;' % (key['label']))
                board_scr.append('MOVE %s (%s %s);' % (
                    key['label'],
                    float_to_str(key['coord'][0]),
                    float_to_str(key['coord'][1])
                ))
                board_scr.append('ROTATE R270 D%s;' % (key['label']))
                board_scr.append('MOVE D%s (%s %s);' % (
                    key['label'],
                    float_to_str(diode_pos[0]),
                    float_to_str(diode_pos[1])
                ))
                board_scr.append('WIRE 16 %s (%s %s) (%s %s);' % (
                    self.trace_width,
                    diode_neg_pos[0],
                    diode_neg_pos[1],
                    float_to_str(sw_pin_0_pos[0]),
                    float_to_str(sw_pin_0_pos[1])
                ))

                # If there's a switch to the left connect our row nets
                if last_key_pos:
                    last_switch_position = (
                        to_imperial(last_key_pos[0]),
                        to_imperial(last_key_pos[1]) * 2
                    )
                    left_net_pos = [
                        last_switch_position[i] + self.sch_net_offset[i]
                        for i in range(2)
                    ]
                    right_net_pos = [
                        switch_position[i] + self.sch_net_offset[i]
                        for i in range(2)
                    ]

                    if left_net_pos[1] == right_net_pos[1]:
                        schematic_scr.append('NET ROW%s (%s %s) (%s %s);' % (
                            row_num,
                            float_to_str(left_net_pos[0]),
                            float_to_str(left_net_pos[1]),
                            float_to_str(right_net_pos[0]),
                            float_to_str(right_net_pos[1])
                        ))
                        left_diode_pos_pos = [
                            last_key_pos[i] + self.layout_diode_pos[i]
                            for i in range(2)
                        ]
                        board_scr.append('WIRE 16 %s (%s %s) (%s %s);' % (
                            self.trace_width,
                            float_to_str(left_diode_pos_pos[0]),
                            float_to_str(left_diode_pos_pos[1]),
                            float_to_str(diode_pos_pos[0]),
                            float_to_str(diode_pos_pos[1])
                        ))

                    else:
                        logging.warn(
                            'Attempting to create invalid ROW net: '
                            'Key:%s Left:%s Right:%s',
                            key['label'], left_net_pos, right_net_pos
                        )

                # Prepare for the next key
                last_key_pos = key['coord']

            # After the last key of the row reset some stuff
            if col_num > maxcol:
                maxcol = col_num

            last_key_pos = None
            col_num = 0
            row_num += 1

        # Connect our columns up
        for column in range(1, maxcol):
            last_key_pos = None
            for row in self.keys:
                try:
                    if column % 2 == 0:
                        key = row.pop(0)
                    else:
                        key = row.pop(-1)
                    key_pos = key['coord']
                except IndexError:
                    last_key_pos = key_pos
                    continue

                if last_key_pos:
                    top_pin_pos = (
                        to_imperial(last_key_pos[0]),
                        to_imperial(last_key_pos[1] * 2)
                    )
                    bot_pin_pos = (
                        to_imperial(key_pos[0]),
                        to_imperial(key_pos[1] * 2)
                    )
                    top_pin_pos = (
                        top_pin_pos[0] + self.sch_col_offset[0],
                        top_pin_pos[1] + self.sch_col_offset[1]
                    )
                    bot_pin_pos = (
                        bot_pin_pos[0] + self.sch_col_offset[0],
                        bot_pin_pos[1] + self.sch_col_offset[1]
                    )
                    top_pin_offset = top_pin_pos[1] - 0.5
                    bot_pin_offset = bot_pin_pos[1] + 0.75

                    schematic_scr.append('NET COLUMN%s (%s %s) (%s %s);' % (
                        column,
                        float_to_str(top_pin_pos[0]),
                        float_to_str(top_pin_pos[1]),
                        float_to_str(top_pin_pos[0]),
                        float_to_str(top_pin_offset)
                    ))
                    schematic_scr.append('NET COLUMN%s (%s %s) (%s %s);' % (
                        column,
                        float_to_str(top_pin_pos[0]),
                        float_to_str(top_pin_offset),
                        float_to_str(bot_pin_pos[0]),
                        float_to_str(bot_pin_offset)
                    ))
                    schematic_scr.append('NET COLUMN%s (%s %s) (%s %s);' % (
                        column,
                        float_to_str(bot_pin_pos[0]),
                        float_to_str(bot_pin_offset),
                        float_to_str(bot_pin_pos[0]),
                        float_to_str(bot_pin_pos[1])
                    ))

                last_key_pos = key_pos

        return schematic_scr, board_scr

    def parse_json(self):
        """Parse the KLE JSON into a data structure we can iterate over.
        """
        self.keys = []
        current_attrs = {
            'coord': [0, 0],
            'next_key': self.default_next_key.copy(),
            'offset': [0, 0],
        }

        for row in self.rawdata:
            if isinstance(row, dict):
                print 'Not reading keyboard properties.'
                continue

            if not isinstance(row, list):
                print "Don't know how to deal with this row:", row
                continue

            self.keys.append([])
            # Each row in our raw data corresponds to a keyboard row.
            current_attrs['coord'][0] = 1
            current_attrs['coord'][1] += 1
            current_attrs['offset'] = [0, 0]

            for item in row:
                if isinstance(item, (str, unicode)):
                    # Prototype our key
                    newkey = deepcopy(current_attrs)
                    newkey['label'] = item.split('\n', 1)[0].upper()
                    newkey['width'] = newkey['next_key']['w']

                    # Apply any key specific offsets
                    newkey['coord'][1] += newkey['next_key']['y']
                    for direction, axis in ('w', 0), ('h', 1):
                        if newkey['next_key'][direction] != 1:
                            offset = newkey['next_key'][direction] - 1
                            logging.debug('Shifting %s along %s by %s',
                                          newkey['label'], direction, offset)
                            newkey['offset'][axis] += offset

                    del(newkey['next_key'])

                    # Flip the Y axis because K-L-E uses an upside-down Y axis
                    newkey['coord'][1] *= -1

                    # Add it to our list of keys
                    self.keys[-1].append(newkey)

                    # Prepare for the next key we'll have to process
                    current_attrs['coord'][0] += current_attrs['next_key']['w']
                    current_attrs['next_key'] = self.default_next_key.copy()

                elif isinstance(item, dict):
                    # This object changes attributes about the next key
                    for attribute, value in item.items():
                        if attribute == 'x':
                            current_attrs['coord'][0] += value

                        elif attribute in ['y', 'w', 'h', 'l', 'n']:
                            current_attrs['next_key'][attribute] = value

                else:
                    print 'Unknown key or object:', item
