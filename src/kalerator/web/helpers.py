import json
import logging
from os import makedirs
from os.path import exists
from flask import render_template
import requests


gist_url = 'https://api.github.com/gists/%s'
layout_url = 'http://www.keyboard-layout-editor.com/layouts/%s'


def fetch_kle_json(storage_type, layout_id):
    """Returns the parsed JSON for a keyboard-layout-editor URL.
    """
    if exists('kle_cache/' + storage_type + layout_id):
        # We have a cached copy, return that instead
        return json.load(open('kle_cache/' + storage_type + layout_id))

    if storage_type == 'layouts':
        keyboard = requests.get(layout_url % layout_id)
        keyboard_text = keyboard.text
        keyboard_json = keyboard.json()
    elif storage_type == 'gists':
        keyboard = requests.get(gist_url % layout_id).json()
        keyboard_text = keyboard['files']['layout.kbd.json']['content']
        keyboard_json = json.loads(keyboard_text)
    else:
        logging.error('Unknown storage_type: %s', storage_type)

    if not exists('kle_cache'):
        makedirs('kle_cache')
    with open('kle_cache/' + storage_type + layout_id, 'w') as fd:
        fd.write(keyboard_text)  # Write this to a cache file

    return keyboard_json


def render_page(page, **args):
    """Returns a rendered template.

    This is a wrapper around render_template() to make it a bit easier to
    deliver templates. It will automatically tack .html onto the end of page
    so your calls are slightly shorter, and it will add the following values
    to args so that this information is always available to your templates:

    * FIXME
    """
    return render_template(page + '.html', **args)
