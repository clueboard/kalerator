import json
import logging
from time import time, strftime, gmtime
from os import makedirs, stat
from os.path import exists
from flask import render_template
import requests


gist_url = 'https://api.github.com/gists/%s'
layout_url = 'http://www.keyboard-layout-editor.com/layouts/%s'


def fetch_kle_json(storage_type, layout_id):
    """Returns the parsed JSON for a keyboard-layout-editor URL.
    """
    cache_file = 'kle_cache/' + storage_type + layout_id
    headers = {}

    if exists(cache_file):
        # We have a cached copy
        file_date = stat(cache_file).st_mtime
        file_age = time() - file_date

        if file_age < 60:
            logging.warning('Cache file %s is %ss old, skipping HTTP check.',
                          cache_file, file_age)
            return json.load(open(cache_file))

        headers['If-Modified-Since'] = strftime('%a, %d %b %Y %H:%M:%S GMT',
                                                gmtime(file_date))
        logging.warning('Adding If-Modified-Since: %s to headers.',
                      headers['If-Modified-Since'])

    if storage_type == 'layouts':
        keyboard = requests.get(layout_url % layout_id, headers=headers)

        if keyboard.status_code == 304:
            logging.debug("Source for %s hasn't changed, loading from disk.",
                          cache_file)
            return json.load(open(cache_file))

        keyboard_text = keyboard.text
        keyboard_json = keyboard.json()

    elif storage_type == 'gists':
        keyboard = requests.get(gist_url % layout_id, headers=headers)

        if keyboard.status_code == 304:
            logging.debug("Source for %s hasn't changed, loading from disk.",
                          cache_file)
            return json.load(open(cache_file))

        keyboard = keyboard.json()

        for file in keyboard['files']:
            keyboard_text = keyboard['files'][file]['content']
            keyboard_json = json.loads(keyboard_text)
            break  # First file wins, hope there's only one...
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
