# coding=UTF-8
from kalerator.config import diode
from kalerator.diode import Diode


def test_Diode():
    """Make sure our diode object works.
    """
    d = Diode('TEST', (0.75, -0.75), (19.05, -19.05), **diode)
    assert d.name == 'TEST'
    assert d.coord_in == (0.65, -0.3)
    assert d.coord_mm == (10.100000000000001, -19.05)
    assert d.footprint == "DIODE'1N4148'@Seeed-OPL-Diode"
    assert d.switch_pin == (16.51, -24.130000000000003)
    assert d.pin_neg == (10.100000000000001, -16.05)
    assert d.pin_pos == (10.100000000000001, -22.05)
    assert d.board_scr == """ROTATE R90 DTEST;
MOVE DTEST (10.10 -19.05);
WIRE 16 0.5 (10.1 -22.05) (16.51 -24.13);"""
    assert d.schematic_scr == \
           "ADD DIODE'1N4148'@Seeed-OPL-Diode DTEST R90 (0.65 -0.30);"

