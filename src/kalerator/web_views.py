from flask import abort, request
from .helpers import render_page, fetch_kle_json
from kalerator import Kalerator
from .web_app import app


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

    kle_json = fetch_kle_json(request.form.get('kle_url'))
    k = Kalerator(kle_json)

    return render_page('show_scripts', keyboard=k)
