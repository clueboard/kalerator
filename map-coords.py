#!/usr/bin/env python
import json
import logging
from argparse import ArgumentParser
from copy import deepcopy
from math import trunc

# Setup our environment
logging.basicConfig()
parser = ArgumentParser(description='Turn KLE into an eagle schematic')
parser.add_argument('file', help='JSON file to process')
args = parser.parse_args()
rawdata = json.loads(open(args.file).read())

# Default values
default_next_key = {
    'y': 0,
    'w': 1,
    'h': 1,
}
device_names = {
    'diode': "DIODE'1N4148'@Seeed-OPL-Diode",
    'diode-smd': "DIODE-GEN-PURPOSE-1KV-1A(DO-214AC)@Seeed-OPL-Diode",
    'mx-switch': 'ALPSMX-1u@AlpsCherry',
    'mx-switch-1': 'ALPSMX-1u@AlpsCherry',
    'mx-switch-1.25': 'ALPSMX-1.25u@AlpsCherry',
    'mx-switch-1.5': 'ALPSMX-1.5u@AlpsCherry',
    'mx-switch-1.75': 'ALPSMX-1.75u@AlpsCherry',
    'mx-switch-2': 'ALPSMX-2u@AlpsCherry',
    'mx-switch-2.25': 'ALPSMX-2.25u@AlpsCherry',
    'mx-switch-2.75': 'ALPSMX-2.75u@AlpsCherry',
    'mx-switch-6': 'ALPSMX-6u@AlpsCherry',
    'mx-switch-6.25': 'ALPSMX-6.25u@AlpsCherry',
    'mx-switch-6.5': 'ALPSMX-6.5u@AlpsCherry',
    'mx-switch-7': 'ALPSMX-7u@AlpsCherry',
}
layout_preamble = """
GRID ON;
GRID MM 1 10;
GRID ALT MM .1;
"""
schematic_preamble = """
SET WIRE_BEND 2;
"""

# Conversion factors
key_spacing = 19.05  # MM
layout_diode_offset = (-8.75, -7)  # MM
layout_sw_pin_0 = (-2.54, -5.08)   # MM
layout_diode_neg = (-8.75, -4)     # MM
layout_diode_pos = (-8.75, -10)    # MM
sch_diode_offset = (-0.1, 0.45)  # IN
sch_net_offset = (-0.1, 0.6)     # IN
sch_col_offset = (-0.3, 0.1)     # IN
trace_width = 0.5


# Functions
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


# Parse the raw data to generate a list of keys
current_attributes = {
    'coord': [0, 0],
    'next_key': default_next_key.copy(),
    'offset': [0, 0],
}
keys = []
for row in rawdata:
    keys.append([])
    # Each row in our raw data corresponds to a keyboard row.
    current_attributes['coord'][0] = 1
    current_attributes['coord'][1] += 1
    current_attributes['offset'] = [0, 0]

    if isinstance(row, dict):
        print 'Not reading keyboard values.'
        continue

    if not isinstance(row, list):
        print "Don't know how to deal with this row:", row
        continue

    for item in row:
        if isinstance(item, (str, unicode)):
            # Prototype our key
            newkey = deepcopy(current_attributes)
            newkey['label'] = item.split('\n', 1)[0].upper()
            newkey['width'] = newkey['next_key']['w']

            # Apply any key specific offsets
            newkey['coord'][1] += newkey['next_key']['y']
            for direction, axis in ('w', 0), ('h', 1):
                if newkey['next_key'][direction] != 1:
                    offset = newkey['next_key'][direction] - 1
                    logging.debug('Shifting %s along %s by %s' % (newkey['label'], direction, offset))
                    newkey['offset'][axis] += offset

            del(newkey['next_key'])

            # Flip the Y axis because K-L-E uses an upside-down Y axis
            newkey['coord'][1] *= -1

            # Add it to our list of keys
            keys[-1].append(newkey)

            # Prepare for the next key we'll have to process
            current_attributes['coord'][0] += current_attributes['next_key']['w']
            current_attributes['next_key'] = default_next_key.copy()

        elif isinstance(item, dict):
            # Process a json object that changes attributes about the next key
            for attribute, value in item.items():
                if attribute == 'x':
                    current_attributes['coord'][0] += value

                elif attribute in ['y', 'w', 'h', 'l', 'n']:
                    current_attributes['next_key'][attribute] = value

        else:
            print 'Unknown key or object:', item

# Generate the scripts
col_num = 0
row_num = 0
maxcol = 0
last_key_pos = None
row_first_key_pos = None
layout_scr = [layout_preamble]
schematic_scr = [schematic_preamble]
for row in keys:
    for key in row:
        col_num += 1
        for axis in 0, 1:
            # Map keyboard units to MM
            key['coord'][axis] *= key_spacing

            # If this key is offset we need to adjust the center of the key
            if key['offset'][axis]:
                offset_mm = key['offset'][axis] * (key_spacing/2)
                key['coord'][axis] += offset_mm

        # Position this switch/diode on the schematic
        switch_position = (to_imperial(key['coord'][0]), to_imperial(key['coord'][1]) * 2)
        diode_position = [switch_position[i] + sch_diode_offset[i] for i in range(2)]
        device_name = 'mx-switch-' + str(key['width'])

        if device_name in device_names:
            device_name = device_names[device_name]

        else:
            device_name = device_names['mx-switch']

        schematic_scr.append('ADD %s %s (%s %s);' % (device_name, key['label'], float_to_str(switch_position[0]), float_to_str(switch_position[1])))
        schematic_scr.append('ADD %s D%s R90 (%s %s);' % (device_names['diode'], key['label'], float_to_str(diode_position[0]), float_to_str(diode_position[1])))
        schematic_scr.append('VALUE D%s 1N4148;' % (key['label']))

        # Position this switch/diode on the board
        diode_pos = [key['coord'][i] + layout_diode_offset[i] for i in range(2)]
        diode_neg_pos = [key['coord'][i] + layout_diode_neg[i] for i in range(2)]
        diode_pos_pos = [key['coord'][i] + layout_diode_pos[i] for i in range(2)]
        sw_pin_0_pos = [key['coord'][i] + layout_sw_pin_0[i] for i in range(2)]

        layout_scr.append('ROTATE R180 %s;' % (key['label']))
        layout_scr.append('MOVE %s (%s %s);' % (key['label'], float_to_str(key['coord'][0]), float_to_str(key['coord'][1])))
        layout_scr.append('ROTATE R270 D%s;' % (key['label']))
        layout_scr.append('MOVE D%s (%s %s);' % (key['label'], float_to_str(diode_pos[0]), float_to_str(diode_pos[1])))
        layout_scr.append('WIRE 16 %s (%s %s) (%s %s);' % (trace_width, diode_neg_pos[0], diode_neg_pos[1], float_to_str(sw_pin_0_pos[0]), float_to_str(sw_pin_0_pos[1])))

        # If there's a switch to the left connect our row nets
        if last_key_pos:
            last_switch_position = (to_imperial(last_key_pos[0]), to_imperial(last_key_pos[1]) * 2)
            left_net_pos = [last_switch_position[i] + sch_net_offset[i] for i in range(2)]
            right_net_pos = [switch_position[i] + sch_net_offset[i] for i in range(2)]

            if left_net_pos[1] == right_net_pos[1]:
                schematic_scr.append('NET ROW%s (%s %s) (%s %s);' % (row_num, float_to_str(left_net_pos[0]), float_to_str(left_net_pos[1]), float_to_str(right_net_pos[0]), float_to_str(right_net_pos[1])))
                left_diode_pos_pos = [last_key_pos[i] + layout_diode_pos[i] for i in range(2)]
                layout_scr.append('WIRE 16 %s (%s %s) (%s %s);' % (trace_width, float_to_str(left_diode_pos_pos[0]), float_to_str(left_diode_pos_pos[1]), float_to_str(diode_pos_pos[0]), float_to_str(diode_pos_pos[1])))

            else:
                logging.warn('Attempting to create invalid ROW net: Key:%s Left:%s Right:%s', key['label'], left_net_pos, right_net_pos)

        else:
            row_first_key_pos = switch_position

        # If this is the last key of the row reset some stuff
        if last_key_pos and last_key_pos[1] != key['coord'][1]:
            if col_num > maxcol:
                maxcol = col_num

            last_key_pos = None
            col_num = 0
            row_num += 1

        # Prepare for the next key
        last_key_pos = key['coord']

# Connect our columns up
for column in range(1, maxcol):
    last_key_pos = None
    for row in keys:
        try:
            if column % 2 == 0:
                key = row.pop(0)  # Hope I don't need to use row later...
            else:
                key = row.pop(-1)
            key_pos = key['coord']
        except IndexError:
            last_key_pos = key_pos
            continue

        if last_key_pos:
            top_pin_pos = (to_imperial(last_key_pos[0]), to_imperial(last_key_pos[1] * 2))
            bot_pin_pos = (to_imperial(key_pos[0]), to_imperial(key_pos[1] * 2))
            top_pin_pos = (top_pin_pos[0] + sch_col_offset[0], top_pin_pos[1] + sch_col_offset[1])
            bot_pin_pos = (bot_pin_pos[0] + sch_col_offset[0], bot_pin_pos[1] + sch_col_offset[1])

            top_pin_offset = top_pin_pos[1] - 0.5
            bot_pin_offset = bot_pin_pos[1] + 0.75

            schematic_scr.append('NET COLUMN%s (%s %s) (%s %s);' % (column, float_to_str(top_pin_pos[0]), float_to_str(top_pin_pos[1]), float_to_str(top_pin_pos[0]), float_to_str(top_pin_offset)))
            schematic_scr.append('NET COLUMN%s (%s %s) (%s %s);' % (column, float_to_str(top_pin_pos[0]), float_to_str(top_pin_offset), float_to_str(bot_pin_pos[0]), float_to_str(bot_pin_offset)))
            schematic_scr.append('NET COLUMN%s (%s %s) (%s %s);' % (column, float_to_str(bot_pin_pos[0]), float_to_str(bot_pin_offset), float_to_str(bot_pin_pos[0]), float_to_str(bot_pin_pos[1])))

        last_key_pos = key_pos

# Write the scripts generate to files
with open(args.file + '.schematic.scr', 'w') as fd:
    fd.seek(0)
    fd.write('\n'.join(schematic_scr))
    fd.write('\n')

with open(args.file + '.board.scr', 'w') as fd:
    fd.seek(0)
    fd.write('\n'.join(layout_scr))
    fd.write('\n')
