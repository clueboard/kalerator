# coding=UTF-8
from kalerator.keyboard_key import KeyboardKey



def test_KeyboardKey():
    """Make sure a single key works.
    """
    next_key = {'w': 1, 'y': 0}
    kk = KeyboardKey('TEST', None, next_key, 'paid', [1,1], 'FIXME: offset support')

    # Printed so that if the test fails you can see the asserts that will pass.
    print 'assert kk.name ==', repr(kk.name)
    print 'assert kk.coord ==', repr(kk.coord)
    print 'assert kk.coord_id ==', repr(kk.coord_in)
    print 'assert kk.coord_mm ==', repr(kk.coord_mm)
    print 'assert kk.footprint ==', repr(kk.footprint)
    print 'assert kk.width ==', repr(kk.width)
    print 'assert kk.column_pin_scr ==', repr(kk.column_pin_scr)
    print 'assert kk.row_pin ==', repr(kk.row_pin)
    print 'assert kk.sch_pin ==', repr(kk.sch_pin)
    print 'assert kk.board_scr ==', repr(kk.board_scr)
    print 'assert kk.schematic_scr ==', repr(kk.schematic_scr)

    assert kk.name == 'TEST'
    assert kk.coord == [1, -1]
    assert kk.coord_in == (0.75, -1.5)
    assert kk.coord_mm == [19.05, -19.05]
    assert kk.footprint == 'ALPSMX-1U-LED@AlpsCherry'
    assert kk.width == 1
    assert kk.column_pin_scr == (0.45, -1.4)
    assert kk.row_pin == (10.3, -16.05)
    assert kk.sch_pin == [0.65, -0.9]
    assert kk.board_scr == 'ROTATE R180 TEST;\nMOVE TEST (19.05 -19.05);\nROTATE R90 DTEST;\nMOVE DTEST (10.10 -19.05);\nWIRE 16 0.5 (10.1 -22.05) (16.51 -24.13);\nMOVE PROW1 (10.12 -14.17);'
    assert kk.schematic_scr == "ADD ALPSMX-1U-LED@AlpsCherry TEST (0.75 -1.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode DTEST R90 (0.65 -1.05);\nADD HEADER-1P-KEYBOARD@Headers PROW1 R90 (0.65 -0.9);\nJUNCTION (0.65 -0.9);\nNAME ROW1 (0.65 -0.9);\n"


def test_KeyboardKey_free():
    """Make sure a single key works when output for the free version of EAGLE.
    """
    next_key = {'w': 1, 'y': 0}
    kk = KeyboardKey('TEST', None, next_key, 'free', [1,1], 'FIXME: offset support')

    # Printed so that if the test fails you can see the asserts that will pass.
    print 'assert kk.name ==', repr(kk.name)
    print 'assert kk.coord ==', repr(kk.coord)
    print 'assert kk.coord_id ==', repr(kk.coord_in)
    print 'assert kk.coord_mm ==', repr(kk.coord_mm)
    print 'assert kk.footprint ==', repr(kk.footprint)
    print 'assert kk.width ==', repr(kk.width)
    print 'assert kk.column_pin_scr ==', repr(kk.column_pin_scr)
    print 'assert kk.row_pin ==', repr(kk.row_pin)
    print 'assert kk.sch_pin ==', repr(kk.sch_pin)
    print 'assert kk.board_scr ==', repr(kk.board_scr)
    print 'assert kk.schematic_scr ==', repr(kk.schematic_scr)

    assert kk.name == 'TEST'
    assert kk.coord == [1, -1]
    assert kk.coord_in == (0.75, -1.5)
    assert kk.coord_mm == [19.05, -19.05]
    assert kk.footprint == 'ALPSMX-1U-LED@AlpsCherry'
    assert kk.width == 1
    assert kk.column_pin_scr == (0.45, -1.4)
    assert kk.row_pin == (10.3, -16.05)
    assert kk.sch_pin == [0.65, -0.9]
    assert kk.board_scr == 'ROTATE R180 TEST;\nMOVE TEST (10.25 93.75);\nROTATE R90 DTEST;\nMOVE DTEST (1.30 93.75);\nWIRE 16 0.5 (1.30 90.75) (7.71 88.67);\nMOVE PROW1 (1.32 98.63);'
    assert kk.schematic_scr == "ADD ALPSMX-1U-LED@AlpsCherry TEST (0.75 -1.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode DTEST R90 (0.65 -1.05);\nADD HEADER-1P-KEYBOARD@Headers PROW1 R90 (0.65 -0.9);\nJUNCTION (0.65 -0.9);\nNAME ROW1 (0.65 -0.9);\n"


def test_KeyboardKey_left_key():
    """Make sure the rows are connected when we have a left_key passed.
    """
    next_key = {'w': 1, 'y': 0}
    kk_l = KeyboardKey('TEST_LEFT', None, next_key, 'paid', [1,1], 'FIXME: offset support')
    kk = KeyboardKey('TEST_RIGHT', kk_l, next_key, 'paid', [2,1], 'FIXME: offset support')

    # Printed so that if the test fails you can see the asserts that will pass.
    print 'assert kk.name ==', repr(kk.name)
    print 'assert kk.coord ==', repr(kk.coord)
    print 'assert kk.coord_id ==', repr(kk.coord_in)
    print 'assert kk.coord_mm ==', repr(kk.coord_mm)
    print 'assert kk.footprint ==', repr(kk.footprint)
    print 'assert kk.width ==', repr(kk.width)
    print 'assert kk.column_pin_scr ==', repr(kk.column_pin_scr)
    print 'assert kk.row_pin ==', repr(kk.row_pin)
    print 'assert kk.sch_pin ==', repr(kk.sch_pin)
    print 'assert kk.board_scr ==', repr(kk.board_scr)
    print 'assert kk.schematic_scr ==', repr(kk.schematic_scr)

    assert kk.name == 'TEST_RIGHT'
    assert kk.coord == [2, -1]
    assert kk.coord_in == (1.5, -1.5)
    assert kk.coord_mm == [38.1, -19.05]
    assert kk.footprint == 'ALPSMX-1U-LED@AlpsCherry'
    assert kk.width == 1
    assert kk.column_pin_scr == (1.2, -1.4)
    assert kk.row_pin == (29.35, -16.05)
    assert kk.sch_pin == [1.4, -0.9]
    assert kk.board_scr == 'ROTATE R180 TEST_RIGHT;\nMOVE TEST_RIGHT (38.10 -19.05);\nROTATE R90 DTEST_RIGHT;\nMOVE DTEST_RIGHT (29.15 -19.05);\nWIRE 16 0.5 (29.15 -22.05) (35.56 -24.13);\nROUTE 0.5 (10.31 -16.05) (29.34 -16.05);'
    assert kk.schematic_scr == "ADD ALPSMX-1U-LED@AlpsCherry TEST_RIGHT (1.50 -1.50);\nADD DIODE'1N4148'@Seeed-OPL-Diode DTEST_RIGHT R90 (1.40 -1.05);\nNET ROW1 (0.65 -0.90) (1.40 -0.90);"
