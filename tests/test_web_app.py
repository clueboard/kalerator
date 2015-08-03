import pytest
from flask import url_for


def test_healthcheck(client):
    res = client.get(url_for('healthcheck'))
    print res
    assert res.status_code == 200
    assert res.data == 'GOOD'
