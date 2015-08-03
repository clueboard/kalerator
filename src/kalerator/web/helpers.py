import json
from os import makedirs
from os.path import exists
from flask import render_template
import requests


layout_url = 'http://www.keyboard-layout-editor.com/layouts/'


def fetch_kle_json(layout_id=None):
    """Returns the parsed JSON for a keyboard-layout-editor URL.
    """
    if exists('kle_cache/' + layout_id):
        # We have a cached copy, return that instead
        return json.load(open('kle_cache/' + layout_id))

    keyboard = requests.get(layout_url + layout_id)

    if not exists('kle_cache'):
        makedirs('kle_cache')
    with open('kle_cache/' + layout_id, 'w') as fd:
        fd.write(keyboard.text)  # Write this to a cache file

    return keyboard.json()


def render_page(page, **args):
    """Returns a rendered template.

    This is a wrapper around render_template() to make it a bit easier to
    deliver templates. It will automatically tack .html onto the end of page
    so your calls are slightly shorter, and it will add the following values
    to args so that this information is always available to your templates:

    * FIXME
    """
    return render_template(page + '.html', **args)
