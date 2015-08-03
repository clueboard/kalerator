from kalerator.web.helpers import render_page


def test_render_page(app):
    test_str = render_page('test_helpers')
    assert test_str == '\n0\n\n1\n'
