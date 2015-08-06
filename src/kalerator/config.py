# coding=UTF-8
cache_time = 15  # Seconds
default_eagle_ver = 'paid'
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
