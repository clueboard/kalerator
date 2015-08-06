# coding=UTF-8
from kalerator.keyboard import Keyboard


def test_Keyboard_iteration():
    """Make sure we can iterate over a Keyboard instance.
    """
    rawdata = [
        ['1', '2', '3'],
        ['4', '5', '6'],
    ]
    k = Keyboard(rawdata)
    keys = []
    for key in k:
        keys.append(key.name)

    assert keys == ['1', '2', '3', '4', '5', '6']


def test_Keyboard():
    """Comprehensive test of the Keyboard Class.
    """
    rawdata = [
        {
            'backcolor': '#ccc',
            'name': 'Keypad',
            'author': 'skullY',
            'notes': 'Keyboard Notes'
        },
        ['Numlock', '/', '*', '-'],
        ['7', '8', '9', {'h': 2, 'dummy': 'To increase code coverage'}, 'Enter'],
        ['4', '5', '6'],
        ['1', '2', '3', {'h': 1.5, 'x': 2}, 'Enter'],
        [{'w': 2}, '0', '', ['Dummy key to increase code coverage']],
        'Dummy row to increase code coverage'
    ]
    k = Keyboard(rawdata)
    schematic, board = k.generate()

    # Printed so that if the test fails you can see the asserts that will pass.
    print 'assert board ==', repr(board)
    print 'assert schematic ==', repr(schematic)

    assert schematic == "GRID ON;\nGRID IN 0.1 1;\nGRID ALT IN 0.01;\nSET WIRE_BEND 2;\n\n\nADD ALPSMX-1U-LED@AlpsCherry NUMLOCK (0.75 -1.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode DNUMLOCK R90 (0.65 -1.05);\nADD ALPSMX-1U-LED@AlpsCherry KP_SLASH (1.50 -1.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode DKP_SLASH R90 (1.40 -1.05);\nNET ROW1.5 (0.65 -0.90) (1.40 -0.90);\nADD ALPSMX-1U-LED@AlpsCherry 8 (2.25 -1.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode D8 R90 (2.15 -1.05);\nNET ROW1.5 (1.40 -0.90) (2.15 -0.90);\nADD ALPSMX-1U-LED@AlpsCherry KP_DASH (3.00 -1.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode DKP_DASH R90 (2.90 -1.05);\nNET ROW1.5 (2.15 -0.90) (2.90 -0.90);\nADD ALPSMX-1U-LED@AlpsCherry 7 (0.75 -3.00);\nADD DIODE'1N4148'@Seeed-OPL-Diode D7 R90 (0.65 -2.55);\nADD ALPSMX-1U-LED@AlpsCherry 8_DUPE (1.50 -3.00);\nADD DIODE'1N4148'@Seeed-OPL-Diode D8_DUPE R90 (1.40 -2.55);\nNET ROW3.0 (0.65 -2.40) (1.40 -2.40);\nADD ALPSMX-1U-LED@AlpsCherry 9 (2.25 -3.00);\nADD DIODE'1N4148'@Seeed-OPL-Diode D9 R90 (2.15 -2.55);\nNET ROW3.0 (1.40 -2.40) (2.15 -2.40);\nADD ALPSMX-1U-LED@AlpsCherry ENTER (3.00 -3.00);\nADD DIODE'1N4148'@Seeed-OPL-Diode DENTER R90 (2.90 -2.55);\nNET ROW3.0 (2.15 -2.40) (2.90 -2.40);\nADD ALPSMX-1U-LED@AlpsCherry 4 (0.75 -4.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode D4 R90 (0.65 -4.05);\nADD ALPSMX-1U-LED@AlpsCherry 5 (1.50 -4.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode D5 R90 (1.40 -4.05);\nNET ROW4.5 (0.65 -3.90) (1.40 -3.90);\nADD ALPSMX-1U-LED@AlpsCherry 6 (2.25 -4.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode D6 R90 (2.15 -4.05);\nNET ROW4.5 (1.40 -3.90) (2.15 -3.90);\nADD ALPSMX-1U-LED@AlpsCherry 1 (0.75 -6.00);\nADD DIODE'1N4148'@Seeed-OPL-Diode D1 R90 (0.65 -5.55);\nADD ALPSMX-1U-LED@AlpsCherry 2 (1.50 -6.00);\nADD DIODE'1N4148'@Seeed-OPL-Diode D2 R90 (1.40 -5.55);\nNET ROW6.0 (0.65 -5.40) (1.40 -5.40);\nADD ALPSMX-1U-LED@AlpsCherry 3 (2.25 -6.00);\nADD DIODE'1N4148'@Seeed-OPL-Diode D3 R90 (2.15 -5.55);\nNET ROW6.0 (1.40 -5.40) (2.15 -5.40);\nADD ALPSMX-1U-LED@AlpsCherry ENTER_DUPE (4.50 -6.00);\nADD DIODE'1N4148'@Seeed-OPL-Diode DENTER_DUPE R90 (4.40 -5.55);\nNET ROW6.0 (2.15 -5.40) (4.40 -5.40);\nADD ALPSMX-2U-LED@AlpsCherry 0 (0.75 -7.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode D0 R90 (0.65 -7.05);\nADD ALPSMX-1U-LED@AlpsCherry SPACE (2.25 -7.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode DSPACE R90 (2.15 -7.05);\nNET ROW7.5 (0.65 -6.90) (2.15 -6.90);\nNET COLUMN1 (0.45 -1.40) (0.45 -1.90);\nNET COLUMN1 (0.45 -1.90) (0.45 -2.15);\nNET COLUMN1 (0.45 -2.15) (0.45 -2.90);\n\nNET COLUMN1 (0.45 -2.90) (0.45 -3.40);\nNET COLUMN1 (0.45 -3.40) (0.45 -3.65);\nNET COLUMN1 (0.45 -3.65) (0.45 -4.40);\n\nNET COLUMN1 (0.45 -4.40) (0.45 -4.90);\nNET COLUMN1 (0.45 -4.90) (0.45 -5.15);\nNET COLUMN1 (0.45 -5.15) (0.45 -5.90);\n\nNET COLUMN1 (0.45 -5.90) (0.45 -6.40);\nNET COLUMN1 (0.45 -6.40) (0.45 -6.65);\nNET COLUMN1 (0.45 -6.65) (0.45 -7.40);\n\nNET COLUMN2 (1.20 -1.40) (1.20 -1.90);\nNET COLUMN2 (1.20 -1.90) (1.20 -2.15);\nNET COLUMN2 (1.20 -2.15) (1.20 -2.90);\n\nNET COLUMN2 (1.20 -2.90) (1.20 -3.40);\nNET COLUMN2 (1.20 -3.40) (1.20 -5.15);\nNET COLUMN2 (1.20 -5.15) (1.20 -5.90);\n\nNET COLUMN3 (1.95 -1.40) (1.95 -1.90);\nNET COLUMN3 (1.95 -1.90) (1.95 -2.15);\nNET COLUMN3 (1.95 -2.15) (1.95 -2.90);\n\nNET COLUMN3 (1.95 -2.90) (1.95 -3.40);\nNET COLUMN3 (1.95 -3.40) (1.20 -3.65);\nNET COLUMN3 (1.20 -3.65) (1.20 -4.40);\n\nNET COLUMN3 (1.20 -4.40) (1.20 -4.90);\nNET COLUMN3 (1.20 -4.90) (1.95 -5.15);\nNET COLUMN3 (1.95 -5.15) (1.95 -5.90);\n\nNET COLUMN4 (2.70 -1.40) (2.70 -1.90);\nNET COLUMN4 (2.70 -1.90) (2.70 -2.15);\nNET COLUMN4 (2.70 -2.15) (2.70 -2.90);\n\nNET COLUMN4 (2.70 -2.90) (2.70 -3.40);\nNET COLUMN4 (2.70 -3.40) (1.95 -3.65);\nNET COLUMN4 (1.95 -3.65) (1.95 -4.40);\n\nNET COLUMN4 (1.95 -4.40) (1.95 -4.90);\nNET COLUMN4 (1.95 -4.90) (4.20 -5.15);\nNET COLUMN4 (4.20 -5.15) (4.20 -5.90);\n\nNET COLUMN4 (4.20 -5.90) (4.20 -6.40);\nNET COLUMN4 (4.20 -6.40) (1.95 -6.65);\nNET COLUMN4 (1.95 -6.65) (1.95 -7.40);\n\n\n\nWINDOW FIT;"
    assert board == 'GRID ON;\nGRID MM 1 10;\nGRID ALT MM .1;\n\n\nROTATE R180 NUMLOCK;\nMOVE NUMLOCK (19.05 -19.05);\nROTATE R90 DNUMLOCK;\nMOVE DNUMLOCK (10.10 -19.05);\nWIRE 16 0.5 (10.1 -22.05) (16.51 -24.13);\nROTATE R180 KP_SLASH;\nMOVE KP_SLASH (38.10 -19.05);\nROTATE R90 DKP_SLASH;\nMOVE DKP_SLASH (29.15 -19.05);\nWIRE 16 0.5 (29.15 -22.05) (35.56 -24.13);\nROUTE 0.5 (10.31 -16.05) (29.34 -16.05);\nROTATE R180 8;\nMOVE 8 (57.15 -19.05);\nROTATE R90 D8;\nMOVE D8 (48.20 -19.05);\nWIRE 16 0.5 (48.2 -22.05) (54.61 -24.13);\nROUTE 0.5 (29.36 -16.05) (48.39 -16.05);\nROTATE R180 KP_DASH;\nMOVE KP_DASH (76.20 -19.05);\nROTATE R90 DKP_DASH;\nMOVE DKP_DASH (67.25 -19.05);\nWIRE 16 0.5 (67.25 -22.05) (73.66 -24.13);\nROUTE 0.5 (48.41 -16.05) (67.44 -16.05);\nROTATE R180 7;\nMOVE 7 (19.05 -38.10);\nROTATE R90 D7;\nMOVE D7 (10.10 -38.10);\nWIRE 16 0.5 (10.1 -41.1) (16.51 -43.18);\nROTATE R180 8_DUPE;\nMOVE 8_DUPE (38.10 -38.10);\nROTATE R90 D8_DUPE;\nMOVE D8_DUPE (29.15 -38.10);\nWIRE 16 0.5 (29.15 -41.1) (35.56 -43.18);\nROUTE 0.5 (10.31 -35.10) (29.34 -35.10);\nROTATE R180 9;\nMOVE 9 (57.15 -38.10);\nROTATE R90 D9;\nMOVE D9 (48.20 -38.10);\nWIRE 16 0.5 (48.2 -41.1) (54.61 -43.18);\nROUTE 0.5 (29.36 -35.10) (48.39 -35.10);\nROTATE R180 ENTER;\nMOVE ENTER (76.20 -38.10);\nROTATE R90 DENTER;\nMOVE DENTER (67.25 -38.10);\nWIRE 16 0.5 (67.25 -41.1) (73.66 -43.18);\nROUTE 0.5 (48.41 -35.10) (67.44 -35.10);\nROTATE R180 4;\nMOVE 4 (19.05 -57.15);\nROTATE R90 D4;\nMOVE D4 (10.10 -57.15);\nWIRE 16 0.5 (10.1 -60.15) (16.51 -62.23);\nROTATE R180 5;\nMOVE 5 (38.10 -57.15);\nROTATE R90 D5;\nMOVE D5 (29.15 -57.15);\nWIRE 16 0.5 (29.15 -60.15) (35.56 -62.23);\nROUTE 0.5 (10.31 -54.15) (29.34 -54.15);\nROTATE R180 6;\nMOVE 6 (57.15 -57.15);\nROTATE R90 D6;\nMOVE D6 (48.20 -57.15);\nWIRE 16 0.5 (48.2 -60.15) (54.61 -62.23);\nROUTE 0.5 (29.36 -54.15) (48.39 -54.15);\nROTATE R180 1;\nMOVE 1 (19.05 -76.20);\nROTATE R90 D1;\nMOVE D1 (10.10 -76.20);\nWIRE 16 0.5 (10.1 -79.2) (16.51 -81.28);\nROTATE R180 2;\nMOVE 2 (38.10 -76.20);\nROTATE R90 D2;\nMOVE D2 (29.15 -76.20);\nWIRE 16 0.5 (29.15 -79.2) (35.56 -81.28);\nROUTE 0.5 (10.31 -73.20) (29.34 -73.20);\nROTATE R180 3;\nMOVE 3 (57.15 -76.20);\nROTATE R90 D3;\nMOVE D3 (48.20 -76.20);\nWIRE 16 0.5 (48.2 -79.2) (54.61 -81.28);\nROUTE 0.5 (29.36 -73.20) (48.39 -73.20);\nROTATE R180 ENTER_DUPE;\nMOVE ENTER_DUPE (114.30 -76.20);\nROTATE R90 DENTER_DUPE;\nMOVE DENTER_DUPE (105.35 -76.20);\nWIRE 16 0.5 (105.35 -79.2) (111.76 -81.28);\nROUTE 0.5 (48.41 -73.20) (105.54 -73.20);\nROTATE R180 0;\nMOVE 0 (28.57 -95.25);\nROTATE R90 D0;\nMOVE D0 (19.62 -95.25);\nWIRE 16 0.5 (19.625 -98.25) (26.03 -100.33);\nROTATE R180 SPACE;\nMOVE SPACE (57.15 -95.25);\nROTATE R90 DSPACE;\nMOVE DSPACE (48.20 -95.25);\nWIRE 16 0.5 (48.2 -98.25) (54.61 -100.33);\nROUTE 0.5 (19.83 -92.25) (48.39 -92.25);\n\n\nRATSNEST;\nWINDOW FIT;'

