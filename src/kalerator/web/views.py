# coding=UTF-8
from urlparse import urlparse
from flask import abort, request, Response, url_for
from .helpers import render_page, fetch_kle_json
from kalerator import config
from kalerator.keyboard import Keyboard
from .app import app
from werkzeug.utils import redirect


@app.route('/', methods=['GET'])
def index():
    """The front page for kalerator.
    """
    return render_page('index')


@app.route('/', methods=['POST'])
def post_index():
    """Redirect to the appropriate view URL.
    """
    if 'kle_url' not in request.form:
        abort(400)  # They aren't giving us the right form data

    eagle_version = request.form.get('eagle_version', config.default_eagle_ver)
    url = urlparse(request.form.get('kle_url'))
    switch_footprint = request.form.get('switch_footprint', 'KEYSWITCH-PLAIN-ALPSMX')
    diode_type = request.form.get('diode_type', 'tht')
    smd_led = request.form.get('smd_led', 'no')

    try:
        storage_type, layout_id = url.fragment.split('/')[1:3]

    except IndexError:
        abort(400)  # They gave us an invalid URL

    return redirect(url_for('view_storage_type_layout_id', storage_type=storage_type, layout_id=layout_id) + '?eagle_version=' + eagle_version + '&switch_footprint=' + switch_footprint + '&diode_type=' + diode_type + '&smd_led=' + smd_led)


@app.route('/view/<storage_type>/<layout_id>', methods=['GET'])
def view_storage_type_layout_id(storage_type, layout_id):
    """View a layout.
    """
    eagle_version = request.args.get('eagle_version', config.default_eagle_ver)
    switch_footprint = request.args.get('switch_footprint', 'KEYSWITCH-PLAIN-ALPSMX')
    diode_type = request.args.get('diode_type', 'tht')
    smd_led = request.args.get('smd_led', 'no')
    kle_json = fetch_kle_json(storage_type, layout_id)
    k = Keyboard(kle_json, eagle_version, switch_footprint, diode_type, smd_led)

    return render_page('show_scripts', keyboard=k, storage_type=storage_type, layout_id=layout_id, eagle_version=eagle_version, switch_footprint=switch_footprint, diode_type=diode_type, smd_led=smd_led)


@app.route('/download/board/<storage_type>/<kle_id>', methods=['GET'])
def download_board_kle_id(storage_type, kle_id):
    """Download the board script.
    """
    eagle_version = request.args.get('eagle_version', config.default_eagle_ver)
    switch_footprint = request.args.get('switch_footprint', 'KEYSWITCH-PLAIN-ALPSMX')
    diode_type = request.args.get('diode_type', 'tht')
    smd_led = request.args.get('smd_led', 'no')
    kle_json = fetch_kle_json(storage_type=storage_type, layout_id=kle_id)
    k = Keyboard(kle_json, eagle_version, switch_footprint, diode_type, smd_led)
    name = k.name if k.name else kle_id

    res = Response(k.board_scr + '\n',
                   mimetype='application/octet-stream')
    res.headers['Content-Disposition'] = \
        'attachment; filename="%s.board.scr"' % name

    return res


@app.route('/download/schematic/<storage_type>/<kle_id>', methods=['GET'])
def download_schematic_kle_id(storage_type, kle_id):
    """Download the schematic script.
    """
    eagle_version = request.args.get('eagle_version', config.default_eagle_ver)
    switch_footprint = request.args.get('switch_footprint', 'KEYSWITCH-PLAIN-ALPSMX')
    diode_type = request.args.get('diode_type', 'tht')
    smd_led = request.args.get('smd_led', 'no')
    kle_json = fetch_kle_json(storage_type=storage_type, layout_id=kle_id)
    k = Keyboard(kle_json, eagle_version, switch_footprint, diode_type, smd_led)
    name = k.name if k.name else kle_id

    res = Response(k.schematic_scr + '\n',
                   mimetype='application/octet-stream')
    res.headers['Content-Disposition'] = \
        'attachment; filename="%s.schematic.scr"' % name

    return res
