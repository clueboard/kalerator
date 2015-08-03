from urlparse import urlparse
from flask import abort, request, Response
from .helpers import render_page, fetch_kle_json
from kalerator.keyboard import Keyboard
from .app import app


@app.route('/', methods=['GET'])
def index():
    """The front page for kalerator.
    """
    return render_page('index')


@app.route('/', methods=['POST'])
def post_index():
    """Do something with the keyboard-layout-editor URL.
    """
    if 'kle_url' not in request.form:
        abort(400)  # They aren't giving us the right form data

    url = urlparse(request.form.get('kle_url'))

    try:
        layout_id = url.fragment.split('/')[2]

    except IndexError:
        abort(400)  # They gave us an invalid URL

    kle_json = fetch_kle_json(layout_id)
    k = Keyboard(kle_json)

    return render_page('show_scripts', keyboard=k, layout_id=layout_id)


@app.route('/download/board/<kle_id>', methods=['GET'])
def download_board_kle_id(kle_id):
    """Download the board script.
    """
    kle_json = fetch_kle_json(layout_id=kle_id)
    k = Keyboard(kle_json)

    res = Response(k.board_scr + '\n',
                   mimetype='application/octet-stream')
    res.headers['Content-Disposition'] = \
        'attachment; filename="%s.board.scr"' % kle_id

    return res


@app.route('/download/schematic/<kle_id>', methods=['GET'])
def download_schematic_kle_id(kle_id):
    """Download the schematic script.
    """
    kle_json = fetch_kle_json(layout_id=kle_id)
    k = Keyboard(kle_json)

    res = Response(k.schematic_scr + '\n',
                   mimetype='application/octet-stream')
    res.headers['Content-Disposition'] = \
        'attachment; filename="%s.schematic.scr"' % kle_id

    return res
