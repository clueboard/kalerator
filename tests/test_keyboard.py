# coding=UTF-8
from kalerator.keyboard import Keyboard


def test_Keyboard_iteration():
    """Make sure we can iterate over a Keyboard instance.
    """
    rawdata = [
        ['1', '2'],
        ['3', '4'],
    ]
    k = Keyboard(rawdata, 'paid')
    keys = []
    for key in k:
        keys.append(key.name)

    assert keys == ['1', '2', '3', '4']


def test_Keyboard_column_board_scr():
    """Test a corner case I probably don't use anywhere.
    """
    rawdata = [
        ['1', '2'],
        ['3', '4'],
    ]
    k = Keyboard(rawdata, 'paid')

    # Printed so that if the test fails you can see the asserts that will pass.
    print 'assert k.column_board_scr ==', repr(k.column_board_scr)

    assert k.column_board_scr == 'MOVE PCOLUMN1 (22.40 -28.60);\nMOVE PCOLUMN2 (41.45 -28.60);'


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
    k = Keyboard(rawdata, 'paid')
    schematic, board = k.generate()

    # Printed so that if the test fails you can see the asserts that will pass.
    print 'assert k.backcolor ==', repr(k.backcolor)
    print 'assert k.name ==', repr(k.name)
    print 'assert k.author ==', repr(k.author)
    print 'assert k.notes ==', repr(k.notes)
    print 'assert board ==', repr(board)
    print 'assert schematic ==', repr(schematic)

    assert k.backcolor == '#ccc'
    assert k.name == 'Keypad'
    assert k.author == 'skullY'
    assert k.notes == 'Keyboard Notes'
    assert board == 'GRID ON;\nGRID MM 1 10;\nGRID ALT MM .1;\n\n\nROTATE R180 NUMLOCK;\nMOVE NUMLOCK (19.05 -19.05);\nROTATE R90 DNUMLOCK;\nMOVE DNUMLOCK (10.10 -19.05);\nWIRE 16 0.5 (10.1 -22.05) (16.51 -24.13);\nMOVE PROW1 (10.12 -14.17);\nROTATE R180 KP_SLASH;\nMOVE KP_SLASH (38.10 -19.05);\nROTATE R90 DKP_SLASH;\nMOVE DKP_SLASH (29.15 -19.05);\nWIRE 16 0.5 (29.15 -22.05) (35.56 -24.13);\nROUTE 0.5 (10.31 -16.05) (29.34 -16.05);\nROTATE R180 8;\nMOVE 8 (57.15 -19.05);\nROTATE R90 D8;\nMOVE D8 (48.20 -19.05);\nWIRE 16 0.5 (48.2 -22.05) (54.61 -24.13);\nROUTE 0.5 (29.36 -16.05) (48.39 -16.05);\nROTATE R180 KP_DASH;\nMOVE KP_DASH (76.20 -19.05);\nROTATE R90 DKP_DASH;\nMOVE DKP_DASH (67.25 -19.05);\nWIRE 16 0.5 (67.25 -22.05) (73.66 -24.13);\nROUTE 0.5 (48.41 -16.05) (67.44 -16.05);\nROTATE R180 7;\nMOVE 7 (19.05 -38.10);\nROTATE R90 D7;\nMOVE D7 (10.10 -38.10);\nWIRE 16 0.5 (10.1 -41.1) (16.51 -43.18);\nMOVE PROW2 (10.12 -33.22);\nROTATE R180 8_DUPE;\nMOVE 8_DUPE (38.10 -38.10);\nROTATE R90 D8_DUPE;\nMOVE D8_DUPE (29.15 -38.10);\nWIRE 16 0.5 (29.15 -41.1) (35.56 -43.18);\nROUTE 0.5 (10.31 -35.10) (29.34 -35.10);\nROTATE R180 9;\nMOVE 9 (57.15 -38.10);\nROTATE R90 D9;\nMOVE D9 (48.20 -38.10);\nWIRE 16 0.5 (48.2 -41.1) (54.61 -43.18);\nROUTE 0.5 (29.36 -35.10) (48.39 -35.10);\nROTATE R180 ENTER;\nMOVE ENTER (76.20 -38.10);\nROTATE R90 DENTER;\nMOVE DENTER (67.25 -38.10);\nWIRE 16 0.5 (67.25 -41.1) (73.66 -43.18);\nROUTE 0.5 (48.41 -35.10) (67.44 -35.10);\nROTATE R180 4;\nMOVE 4 (19.05 -57.15);\nROTATE R90 D4;\nMOVE D4 (10.10 -57.15);\nWIRE 16 0.5 (10.1 -60.15) (16.51 -62.23);\nMOVE PROW3 (10.12 -52.27);\nROTATE R180 5;\nMOVE 5 (38.10 -57.15);\nROTATE R90 D5;\nMOVE D5 (29.15 -57.15);\nWIRE 16 0.5 (29.15 -60.15) (35.56 -62.23);\nROUTE 0.5 (10.31 -54.15) (29.34 -54.15);\nROTATE R180 6;\nMOVE 6 (57.15 -57.15);\nROTATE R90 D6;\nMOVE D6 (48.20 -57.15);\nWIRE 16 0.5 (48.2 -60.15) (54.61 -62.23);\nROUTE 0.5 (29.36 -54.15) (48.39 -54.15);\nROTATE R180 1;\nMOVE 1 (19.05 -76.20);\nROTATE R90 D1;\nMOVE D1 (10.10 -76.20);\nWIRE 16 0.5 (10.1 -79.2) (16.51 -81.28);\nMOVE PROW4 (10.12 -71.32);\nROTATE R180 2;\nMOVE 2 (38.10 -76.20);\nROTATE R90 D2;\nMOVE D2 (29.15 -76.20);\nWIRE 16 0.5 (29.15 -79.2) (35.56 -81.28);\nROUTE 0.5 (10.31 -73.20) (29.34 -73.20);\nROTATE R180 3;\nMOVE 3 (57.15 -76.20);\nROTATE R90 D3;\nMOVE D3 (48.20 -76.20);\nWIRE 16 0.5 (48.2 -79.2) (54.61 -81.28);\nROUTE 0.5 (29.36 -73.20) (48.39 -73.20);\nROTATE R180 ENTER_DUPE;\nMOVE ENTER_DUPE (114.30 -76.20);\nROTATE R90 DENTER_DUPE;\nMOVE DENTER_DUPE (105.35 -76.20);\nWIRE 16 0.5 (105.35 -79.2) (111.76 -81.28);\nROUTE 0.5 (48.41 -73.20) (105.54 -73.20);\nROTATE R180 0;\nMOVE 0 (28.57 -95.25);\nROTATE R90 D0;\nMOVE D0 (19.62 -95.25);\nWIRE 16 0.5 (19.625 -98.25) (26.03 -100.33);\nMOVE PROW5 (19.645 -90.37);\nROTATE R180 SPACE;\nMOVE SPACE (57.15 -95.25);\nROTATE R90 DSPACE;\nMOVE DSPACE (48.20 -95.25);\nWIRE 16 0.5 (48.2 -98.25) (54.61 -100.33);\nROUTE 0.5 (19.83 -92.25) (48.39 -92.25);\nMOVE PCOLUMN1 (22.40 -28.60);\nMOVE PCOLUMN2 (41.45 -28.60);\nMOVE PCOLUMN3 (60.50 -28.60);\nMOVE PCOLUMN4 (79.55 -28.60);\n\n\nRATSNEST;\nWINDOW FIT;'
    assert schematic == "GRID ON;\nGRID IN 0.1 1;\nGRID ALT IN 0.01;\nSET WIRE_BEND 2;\n\n\nADD ALPSMX-1U-LED@AlpsCherry NUMLOCK (0.75 -1.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode DNUMLOCK R90 (0.65 -1.05);\nADD HEADER-1P-KEYBOARD@Headers PROW1 R90 (0.65 -0.9);\nJUNCTION (0.65 -0.9);\nNAME ROW1 (0.65 -0.9);\n\nADD ALPSMX-1U-LED@AlpsCherry KP_SLASH (1.50 -1.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode DKP_SLASH R90 (1.40 -1.05);\nNET ROW1 (0.65 -0.90) (1.40 -0.90);\nADD ALPSMX-1U-LED@AlpsCherry 8 (2.25 -1.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode D8 R90 (2.15 -1.05);\nNET ROW1 (1.40 -0.90) (2.15 -0.90);\nADD ALPSMX-1U-LED@AlpsCherry KP_DASH (3.00 -1.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode DKP_DASH R90 (2.90 -1.05);\nNET ROW1 (2.15 -0.90) (2.90 -0.90);\nADD ALPSMX-1U-LED@AlpsCherry 7 (0.75 -3.00);\nADD DIODE'1N4148'@Seeed-OPL-Diode D7 R90 (0.65 -2.55);\nADD HEADER-1P-KEYBOARD@Headers PROW2 R90 (0.65 -2.4);\nJUNCTION (0.65 -2.4);\nNAME ROW2 (0.65 -2.4);\n\nADD ALPSMX-1U-LED@AlpsCherry 8_DUPE (1.50 -3.00);\nADD DIODE'1N4148'@Seeed-OPL-Diode D8_DUPE R90 (1.40 -2.55);\nNET ROW2 (0.65 -2.40) (1.40 -2.40);\nADD ALPSMX-1U-LED@AlpsCherry 9 (2.25 -3.00);\nADD DIODE'1N4148'@Seeed-OPL-Diode D9 R90 (2.15 -2.55);\nNET ROW2 (1.40 -2.40) (2.15 -2.40);\nADD ALPSMX-1U-LED@AlpsCherry ENTER (3.00 -3.00);\nADD DIODE'1N4148'@Seeed-OPL-Diode DENTER R90 (2.90 -2.55);\nNET ROW2 (2.15 -2.40) (2.90 -2.40);\nADD ALPSMX-1U-LED@AlpsCherry 4 (0.75 -4.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode D4 R90 (0.65 -4.05);\nADD HEADER-1P-KEYBOARD@Headers PROW3 R90 (0.65 -3.9);\nJUNCTION (0.65 -3.9);\nNAME ROW3 (0.65 -3.9);\n\nADD ALPSMX-1U-LED@AlpsCherry 5 (1.50 -4.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode D5 R90 (1.40 -4.05);\nNET ROW3 (0.65 -3.90) (1.40 -3.90);\nADD ALPSMX-1U-LED@AlpsCherry 6 (2.25 -4.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode D6 R90 (2.15 -4.05);\nNET ROW3 (1.40 -3.90) (2.15 -3.90);\nADD ALPSMX-1U-LED@AlpsCherry 1 (0.75 -6.00);\nADD DIODE'1N4148'@Seeed-OPL-Diode D1 R90 (0.65 -5.55);\nADD HEADER-1P-KEYBOARD@Headers PROW4 R90 (0.65 -5.4);\nJUNCTION (0.65 -5.4);\nNAME ROW4 (0.65 -5.4);\n\nADD ALPSMX-1U-LED@AlpsCherry 2 (1.50 -6.00);\nADD DIODE'1N4148'@Seeed-OPL-Diode D2 R90 (1.40 -5.55);\nNET ROW4 (0.65 -5.40) (1.40 -5.40);\nADD ALPSMX-1U-LED@AlpsCherry 3 (2.25 -6.00);\nADD DIODE'1N4148'@Seeed-OPL-Diode D3 R90 (2.15 -5.55);\nNET ROW4 (1.40 -5.40) (2.15 -5.40);\nADD ALPSMX-1U-LED@AlpsCherry ENTER_DUPE (4.50 -6.00);\nADD DIODE'1N4148'@Seeed-OPL-Diode DENTER_DUPE R90 (4.40 -5.55);\nNET ROW4 (2.15 -5.40) (4.40 -5.40);\nADD ALPSMX-2U-LED@AlpsCherry 0 (0.75 -7.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode D0 R90 (0.65 -7.05);\nADD HEADER-1P-KEYBOARD@Headers PROW5 R90 (0.65 -6.9);\nJUNCTION (0.65 -6.9);\nNAME ROW5 (0.65 -6.9);\n\nADD ALPSMX-1U-LED@AlpsCherry SPACE (2.25 -7.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode DSPACE R90 (2.15 -7.05);\nNET ROW5 (0.65 -6.90) (2.15 -6.90);\nADD HEADER-1P-KEYBOARD@Headers PCOLUMN1 R180 (0.45 -1.40);\nJUNCTION (0.45 -1.40);\nNAME COLUMN1 (0.45 -1.40);\nNET COLUMN1 (0.45 -1.40) (0.45 -1.90);\nNET COLUMN1 (0.45 -1.90) (0.45 -2.15);\nNET COLUMN1 (0.45 -2.15) (0.45 -2.90);\nNET COLUMN1 (0.45 -2.90) (0.45 -3.40);\nNET COLUMN1 (0.45 -3.40) (0.45 -3.65);\nNET COLUMN1 (0.45 -3.65) (0.45 -4.40);\nNET COLUMN1 (0.45 -4.40) (0.45 -4.90);\nNET COLUMN1 (0.45 -4.90) (0.45 -5.15);\nNET COLUMN1 (0.45 -5.15) (0.45 -5.90);\nNET COLUMN1 (0.45 -5.90) (0.45 -6.40);\nNET COLUMN1 (0.45 -6.40) (0.45 -6.65);\nNET COLUMN1 (0.45 -6.65) (0.45 -7.40);\nADD HEADER-1P-KEYBOARD@Headers PCOLUMN2 R180 (1.20 -1.40);\nJUNCTION (1.20 -1.40);\nNAME COLUMN2 (1.20 -1.40);\nNET COLUMN2 (1.20 -1.40) (1.20 -1.90);\nNET COLUMN2 (1.20 -1.90) (1.20 -2.15);\nNET COLUMN2 (1.20 -2.15) (1.20 -2.90);\nNET COLUMN2 (1.20 -2.90) (1.20 -3.40);\nNET COLUMN2 (1.20 -3.40) (1.20 -5.15);\nNET COLUMN2 (1.20 -5.15) (1.20 -5.90);\nADD HEADER-1P-KEYBOARD@Headers PCOLUMN3 R180 (1.95 -1.40);\nJUNCTION (1.95 -1.40);\nNAME COLUMN3 (1.95 -1.40);\nNET COLUMN3 (1.95 -1.40) (1.95 -1.90);\nNET COLUMN3 (1.95 -1.90) (1.95 -2.15);\nNET COLUMN3 (1.95 -2.15) (1.95 -2.90);\nNET COLUMN3 (1.95 -2.90) (1.95 -3.40);\nNET COLUMN3 (1.95 -3.40) (1.20 -3.65);\nNET COLUMN3 (1.20 -3.65) (1.20 -4.40);\nNET COLUMN3 (1.20 -4.40) (1.20 -4.90);\nNET COLUMN3 (1.20 -4.90) (1.95 -5.15);\nNET COLUMN3 (1.95 -5.15) (1.95 -5.90);\nADD HEADER-1P-KEYBOARD@Headers PCOLUMN4 R180 (2.70 -1.40);\nJUNCTION (2.70 -1.40);\nNAME COLUMN4 (2.70 -1.40);\nNET COLUMN4 (2.70 -1.40) (2.70 -1.90);\nNET COLUMN4 (2.70 -1.90) (2.70 -2.15);\nNET COLUMN4 (2.70 -2.15) (2.70 -2.90);\nNET COLUMN4 (2.70 -2.90) (2.70 -3.40);\nNET COLUMN4 (2.70 -3.40) (1.95 -3.65);\nNET COLUMN4 (1.95 -3.65) (1.95 -4.40);\nNET COLUMN4 (1.95 -4.40) (1.95 -4.90);\nNET COLUMN4 (1.95 -4.90) (4.20 -5.15);\nNET COLUMN4 (4.20 -5.15) (4.20 -5.90);\nNET COLUMN4 (4.20 -5.90) (4.20 -6.40);\nNET COLUMN4 (4.20 -6.40) (1.95 -6.65);\nNET COLUMN4 (1.95 -6.65) (1.95 -7.40);\n\n\nWINDOW FIT;"


def test_Keyboard_free():
    """Comprehensive test of the Keyboard Class for the free version.
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
    k = Keyboard(rawdata, 'free')
    schematic, board = k.generate()

    # Printed so that if the test fails you can see the asserts that will pass.
    print 'assert board ==', repr(board)
    print 'assert schematic ==', repr(schematic)

    assert board == 'GRID ON;\nGRID MM 1 10;\nGRID ALT MM .1;\n\n\nROTATE R180 NUMLOCK;\nMOVE NUMLOCK (10.25 93.75);\nROTATE R90 DNUMLOCK;\nMOVE DNUMLOCK (1.30 93.75);\nWIRE 16 0.5 (1.30 90.75) (7.71 88.67);\nMOVE PROW1 (1.32 98.63);\nROTATE R180 KP_SLASH;\nMOVE KP_SLASH (29.30 93.75);\nROTATE R90 DKP_SLASH;\nMOVE DKP_SLASH (20.35 93.75);\nWIRE 16 0.5 (20.35 90.75) (26.76 88.67);\nROUTE 0.5 (1.51 96.75) (20.54 96.75);\nROTATE R180 8;\nMOVE 8 (48.35 93.75);\nROTATE R90 D8;\nMOVE D8 (39.40 93.75);\nWIRE 16 0.5 (39.40 90.75) (45.81 88.67);\nROUTE 0.5 (20.56 96.75) (39.59 96.75);\nROTATE R180 KP_DASH;\nMOVE KP_DASH (67.40 93.75);\nROTATE R90 DKP_DASH;\nMOVE DKP_DASH (58.45 93.75);\nWIRE 16 0.5 (58.45 90.75) (64.86 88.67);\nROUTE 0.5 (39.61 96.75) (58.64 96.75);\nROTATE R180 7;\nMOVE 7 (10.25 74.70);\nROTATE R90 D7;\nMOVE D7 (1.30 74.70);\nWIRE 16 0.5 (1.30 71.70) (7.71 69.62);\nMOVE PROW2 (1.32 79.58);\nROTATE R180 8_DUPE;\nMOVE 8_DUPE (29.30 74.70);\nROTATE R90 D8_DUPE;\nMOVE D8_DUPE (20.35 74.70);\nWIRE 16 0.5 (20.35 71.70) (26.76 69.62);\nROUTE 0.5 (1.51 77.70) (20.54 77.70);\nROTATE R180 9;\nMOVE 9 (48.35 74.70);\nROTATE R90 D9;\nMOVE D9 (39.40 74.70);\nWIRE 16 0.5 (39.40 71.70) (45.81 69.62);\nROUTE 0.5 (20.56 77.70) (39.59 77.70);\nROTATE R180 ENTER;\nMOVE ENTER (67.40 74.70);\nROTATE R90 DENTER;\nMOVE DENTER (58.45 74.70);\nWIRE 16 0.5 (58.45 71.70) (64.86 69.62);\nROUTE 0.5 (39.61 77.70) (58.64 77.70);\nROTATE R180 4;\nMOVE 4 (10.25 55.65);\nROTATE R90 D4;\nMOVE D4 (1.30 55.65);\nWIRE 16 0.5 (1.30 52.65) (7.71 50.57);\nMOVE PROW3 (1.32 60.53);\nROTATE R180 5;\nMOVE 5 (29.30 55.65);\nROTATE R90 D5;\nMOVE D5 (20.35 55.65);\nWIRE 16 0.5 (20.35 52.65) (26.76 50.57);\nROUTE 0.5 (1.51 58.65) (20.54 58.65);\nROTATE R180 6;\nMOVE 6 (48.35 55.65);\nROTATE R90 D6;\nMOVE D6 (39.40 55.65);\nWIRE 16 0.5 (39.40 52.65) (45.81 50.57);\nROUTE 0.5 (20.56 58.65) (39.59 58.65);\nROTATE R180 1;\nMOVE 1 (10.25 36.60);\nROTATE R90 D1;\nMOVE D1 (1.30 36.60);\nWIRE 16 0.5 (1.30 33.60) (7.71 31.52);\nMOVE PROW4 (1.32 41.48);\nROTATE R180 2;\nMOVE 2 (29.30 36.60);\nROTATE R90 D2;\nMOVE D2 (20.35 36.60);\nWIRE 16 0.5 (20.35 33.60) (26.76 31.52);\nROUTE 0.5 (1.51 39.60) (20.54 39.60);\nROTATE R180 3;\nMOVE 3 (48.35 36.60);\nROTATE R90 D3;\nMOVE D3 (39.40 36.60);\nWIRE 16 0.5 (39.40 33.60) (45.81 31.52);\nROUTE 0.5 (20.56 39.60) (39.59 39.60);\nROTATE R180 ENTER_DUPE;\nMOVE ENTER_DUPE (105.50 36.60);\nROTATE R90 DENTER_DUPE;\nMOVE DENTER_DUPE (96.55 36.60);\nWIRE 16 0.5 (96.55 33.60) (102.96 31.52);\nROUTE 0.5 (39.61 39.60) (96.74 39.60);\nROTATE R180 0;\nMOVE 0 (19.77 17.55);\nROTATE R90 D0;\nMOVE D0 (10.82 17.55);\nWIRE 16 0.5 (10.82 14.55) (17.23 12.47);\nMOVE PROW5 (10.84 22.43);\nROTATE R180 SPACE;\nMOVE SPACE (48.35 17.55);\nROTATE R90 DSPACE;\nMOVE DSPACE (39.40 17.55);\nWIRE 16 0.5 (39.40 14.55) (45.81 12.47);\nROUTE 0.5 (11.03 20.55) (39.59 20.55);\nMOVE PCOLUMN1 (13.60 84.20);\nMOVE PCOLUMN2 (32.65 84.20);\nMOVE PCOLUMN3 (51.70 84.20);\nMOVE PCOLUMN4 (70.75 84.20);\n\n\nRATSNEST;\nWINDOW FIT;'
    assert schematic == "GRID ON;\nGRID IN 0.1 1;\nGRID ALT IN 0.01;\nSET WIRE_BEND 2;\n\n\nADD ALPSMX-1U-LED@AlpsCherry NUMLOCK (0.75 -1.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode DNUMLOCK R90 (0.65 -1.05);\nADD HEADER-1P-KEYBOARD@Headers PROW1 R90 (0.65 -0.9);\nJUNCTION (0.65 -0.9);\nNAME ROW1 (0.65 -0.9);\n\nADD ALPSMX-1U-LED@AlpsCherry KP_SLASH (1.50 -1.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode DKP_SLASH R90 (1.40 -1.05);\nNET ROW1 (0.65 -0.90) (1.40 -0.90);\nADD ALPSMX-1U-LED@AlpsCherry 8 (2.25 -1.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode D8 R90 (2.15 -1.05);\nNET ROW1 (1.40 -0.90) (2.15 -0.90);\nADD ALPSMX-1U-LED@AlpsCherry KP_DASH (3.00 -1.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode DKP_DASH R90 (2.90 -1.05);\nNET ROW1 (2.15 -0.90) (2.90 -0.90);\nADD ALPSMX-1U-LED@AlpsCherry 7 (0.75 -3.00);\nADD DIODE'1N4148'@Seeed-OPL-Diode D7 R90 (0.65 -2.55);\nADD HEADER-1P-KEYBOARD@Headers PROW2 R90 (0.65 -2.4);\nJUNCTION (0.65 -2.4);\nNAME ROW2 (0.65 -2.4);\n\nADD ALPSMX-1U-LED@AlpsCherry 8_DUPE (1.50 -3.00);\nADD DIODE'1N4148'@Seeed-OPL-Diode D8_DUPE R90 (1.40 -2.55);\nNET ROW2 (0.65 -2.40) (1.40 -2.40);\nADD ALPSMX-1U-LED@AlpsCherry 9 (2.25 -3.00);\nADD DIODE'1N4148'@Seeed-OPL-Diode D9 R90 (2.15 -2.55);\nNET ROW2 (1.40 -2.40) (2.15 -2.40);\nADD ALPSMX-1U-LED@AlpsCherry ENTER (3.00 -3.00);\nADD DIODE'1N4148'@Seeed-OPL-Diode DENTER R90 (2.90 -2.55);\nNET ROW2 (2.15 -2.40) (2.90 -2.40);\nADD ALPSMX-1U-LED@AlpsCherry 4 (0.75 -4.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode D4 R90 (0.65 -4.05);\nADD HEADER-1P-KEYBOARD@Headers PROW3 R90 (0.65 -3.9);\nJUNCTION (0.65 -3.9);\nNAME ROW3 (0.65 -3.9);\n\nADD ALPSMX-1U-LED@AlpsCherry 5 (1.50 -4.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode D5 R90 (1.40 -4.05);\nNET ROW3 (0.65 -3.90) (1.40 -3.90);\nADD ALPSMX-1U-LED@AlpsCherry 6 (2.25 -4.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode D6 R90 (2.15 -4.05);\nNET ROW3 (1.40 -3.90) (2.15 -3.90);\nADD ALPSMX-1U-LED@AlpsCherry 1 (0.75 -6.00);\nADD DIODE'1N4148'@Seeed-OPL-Diode D1 R90 (0.65 -5.55);\nADD HEADER-1P-KEYBOARD@Headers PROW4 R90 (0.65 -5.4);\nJUNCTION (0.65 -5.4);\nNAME ROW4 (0.65 -5.4);\n\nADD ALPSMX-1U-LED@AlpsCherry 2 (1.50 -6.00);\nADD DIODE'1N4148'@Seeed-OPL-Diode D2 R90 (1.40 -5.55);\nNET ROW4 (0.65 -5.40) (1.40 -5.40);\nADD ALPSMX-1U-LED@AlpsCherry 3 (2.25 -6.00);\nADD DIODE'1N4148'@Seeed-OPL-Diode D3 R90 (2.15 -5.55);\nNET ROW4 (1.40 -5.40) (2.15 -5.40);\nADD ALPSMX-1U-LED@AlpsCherry ENTER_DUPE (4.50 -6.00);\nADD DIODE'1N4148'@Seeed-OPL-Diode DENTER_DUPE R90 (4.40 -5.55);\nNET ROW4 (2.15 -5.40) (4.40 -5.40);\nADD ALPSMX-2U-LED@AlpsCherry 0 (0.75 -7.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode D0 R90 (0.65 -7.05);\nADD HEADER-1P-KEYBOARD@Headers PROW5 R90 (0.65 -6.9);\nJUNCTION (0.65 -6.9);\nNAME ROW5 (0.65 -6.9);\n\nADD ALPSMX-1U-LED@AlpsCherry SPACE (2.25 -7.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode DSPACE R90 (2.15 -7.05);\nNET ROW5 (0.65 -6.90) (2.15 -6.90);\nADD HEADER-1P-KEYBOARD@Headers PCOLUMN1 R180 (0.45 -1.40);\nJUNCTION (0.45 -1.40);\nNAME COLUMN1 (0.45 -1.40);\nNET COLUMN1 (0.45 -1.40) (0.45 -1.90);\nNET COLUMN1 (0.45 -1.90) (0.45 -2.15);\nNET COLUMN1 (0.45 -2.15) (0.45 -2.90);\nNET COLUMN1 (0.45 -2.90) (0.45 -3.40);\nNET COLUMN1 (0.45 -3.40) (0.45 -3.65);\nNET COLUMN1 (0.45 -3.65) (0.45 -4.40);\nNET COLUMN1 (0.45 -4.40) (0.45 -4.90);\nNET COLUMN1 (0.45 -4.90) (0.45 -5.15);\nNET COLUMN1 (0.45 -5.15) (0.45 -5.90);\nNET COLUMN1 (0.45 -5.90) (0.45 -6.40);\nNET COLUMN1 (0.45 -6.40) (0.45 -6.65);\nNET COLUMN1 (0.45 -6.65) (0.45 -7.40);\nADD HEADER-1P-KEYBOARD@Headers PCOLUMN2 R180 (1.20 -1.40);\nJUNCTION (1.20 -1.40);\nNAME COLUMN2 (1.20 -1.40);\nNET COLUMN2 (1.20 -1.40) (1.20 -1.90);\nNET COLUMN2 (1.20 -1.90) (1.20 -2.15);\nNET COLUMN2 (1.20 -2.15) (1.20 -2.90);\nNET COLUMN2 (1.20 -2.90) (1.20 -3.40);\nNET COLUMN2 (1.20 -3.40) (1.20 -5.15);\nNET COLUMN2 (1.20 -5.15) (1.20 -5.90);\nADD HEADER-1P-KEYBOARD@Headers PCOLUMN3 R180 (1.95 -1.40);\nJUNCTION (1.95 -1.40);\nNAME COLUMN3 (1.95 -1.40);\nNET COLUMN3 (1.95 -1.40) (1.95 -1.90);\nNET COLUMN3 (1.95 -1.90) (1.95 -2.15);\nNET COLUMN3 (1.95 -2.15) (1.95 -2.90);\nNET COLUMN3 (1.95 -2.90) (1.95 -3.40);\nNET COLUMN3 (1.95 -3.40) (1.20 -3.65);\nNET COLUMN3 (1.20 -3.65) (1.20 -4.40);\nNET COLUMN3 (1.20 -4.40) (1.20 -4.90);\nNET COLUMN3 (1.20 -4.90) (1.95 -5.15);\nNET COLUMN3 (1.95 -5.15) (1.95 -5.90);\nADD HEADER-1P-KEYBOARD@Headers PCOLUMN4 R180 (2.70 -1.40);\nJUNCTION (2.70 -1.40);\nNAME COLUMN4 (2.70 -1.40);\nNET COLUMN4 (2.70 -1.40) (2.70 -1.90);\nNET COLUMN4 (2.70 -1.90) (2.70 -2.15);\nNET COLUMN4 (2.70 -2.15) (2.70 -2.90);\nNET COLUMN4 (2.70 -2.90) (2.70 -3.40);\nNET COLUMN4 (2.70 -3.40) (1.95 -3.65);\nNET COLUMN4 (1.95 -3.65) (1.95 -4.40);\nNET COLUMN4 (1.95 -4.40) (1.95 -4.90);\nNET COLUMN4 (1.95 -4.90) (4.20 -5.15);\nNET COLUMN4 (4.20 -5.15) (4.20 -5.90);\nNET COLUMN4 (4.20 -5.90) (4.20 -6.40);\nNET COLUMN4 (4.20 -6.40) (1.95 -6.65);\nNET COLUMN4 (1.95 -6.65) (1.95 -7.40);\n\n\nWINDOW FIT;"
