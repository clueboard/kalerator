# coding=UTF-8
import logging
from kalerator import config
import requests
from codecs import open as copen
from flask import render_template
from time import time, strftime, localtime
from os import makedirs, remove, stat
from os.path import exists


cache_dir = 'kle_cache'
gist_url = 'https://api.github.com/gists/%s'
layout_url = 'http://www.keyboard-layout-editor.com/layouts/%s'


def fetch_kle_json(storage_type, layout_id):
    """Returns the JSON for a keyboard-layout-editor URL.
    """
    cache_file = cache_dir + '/' + storage_type + '-' + layout_id
    headers = {}

    if exists(cache_file):
        # We have a cached copy
        file_stat = stat(cache_file)
        file_date = file_stat.st_mtime
        file_size = file_stat.st_size
        file_age = time() - file_date

        if file_size == 0:
            # Invalid cache
            logging.warning('Removing zero-length cache file %s', cache_file)
            remove(cache_file)

        elif file_age < config.cache_time:
            logging.warning('Cache file %s is %ss old, skipping HTTP check.',
                            cache_file, file_age)
            return copen(cache_file, encoding='UTF-8').read()

        else:
            headers['If-Modified-Since'] = strftime('%a, %d %b %Y %H:%M:%S %Z',
                                                    localtime(file_date))
            logging.warning('Adding If-Modified-Since: %s to headers.',
                            headers['If-Modified-Since'])

    if storage_type == 'layouts':
        keyboard = requests.get(layout_url % layout_id, headers=headers)

        if keyboard.status_code == 304:
            logging.debug("Source for %s hasn't changed, loading from disk.",
                          cache_file)
            return copen(cache_file, encoding='UTF-8').read()

        keyboard_text = keyboard.text

    elif storage_type == 'gists':
        keyboard = requests.get(gist_url % layout_id, headers=headers)

        if keyboard.status_code == 304:
            logging.debug("Source for %s hasn't changed, loading from disk.",
                          cache_file)
            return copen(cache_file, encoding='UTF-8').read()

        keyboard = keyboard.json()

        for file in keyboard['files']:
            keyboard_text = keyboard['files'][file]['content']
            break  # First file wins, hope there's only one...
    else:
        logging.error('Unknown storage_type: %s', storage_type)

    if not exists(cache_dir):
        makedirs(cache_dir)

    with copen(cache_file, 'w', encoding='UTF-8') as fd:
        fd.write(keyboard_text)  # Write this to a cache file

    return keyboard_text


def render_page(page, **args):
    """Returns a rendered template.

    This is a wrapper around render_template() to make it a bit easier to
    deliver templates. It will automatically tack .html onto the end of page
    so your calls are slightly shorter, and it will add the following values
    to args so that this information is always available to your templates:

    * FIXME
    """
    return render_template(page + '.html', **args)
