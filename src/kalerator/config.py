# coding=UTF-8
from decimal import Decimal

cache_time = 15  # Seconds
default_eagle_ver = 'paid'
key_spacing_mm = Decimal('19.05')
key_spacing_in = Decimal('0.75')
trace_width = Decimal('0.5')  # MM
diode = {
    'tht': {
        'footprint': "DIODE-DO-35",
        'switch_offset_board': (Decimal('-8.95'), Decimal('0')),
        'switch_offset_schematic': (Decimal('-0.1'), Decimal('0.5')),
        'switch_pin_offset': (Decimal('-2.54'), Decimal('-5.08')),
        'pin_neg_offset': (Decimal('0'), Decimal('3')),
        'pin_pos_offset': (Decimal('0'), Decimal('-3')),
    },
    'smd': {
        'footprint': "DIODE-SOD-123",
        'switch_offset_board': (Decimal('-8.89'), Decimal('-6.16')),
        'switch_offset_schematic': (Decimal('-0.1'), Decimal('0.5')),
        'switch_pin_offset': (Decimal('-2.54'), Decimal('-5.08')),
        'pin_neg_offset': (Decimal('0'), Decimal('3')),
        'pin_pos_offset': (Decimal('0'), Decimal('-3')),
    }
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
