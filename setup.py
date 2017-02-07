#!/usr/bin/env python
# Special thanks to Hynek Schlawack for providing excellent documentation:
#
# https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
import os
from setuptools import setup, find_packages, Command


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()


setup(
    name='kalerator',
    version='0.0.1',
    description='Web tool for turning keyboard-layout-editor into EAGLE script',
    long_description='\n\n'.join((read('README.rst'), read('AUTHORS.rst'))),
    url='http://kalerator.clueboard.co/',
    license='all_rights_reserved',
    author='skullY',
    author_email='skullydazed@gmail.com',
    install_requires=['flask', 'flask-csrf', 'greenlet', 'gevent', 'requests', 'kle2xy'], 
    packages=find_packages(),
    scripts=['bin/kle'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: Restrictive',
        'Topic :: System :: Systems Administration',
    ],
)
