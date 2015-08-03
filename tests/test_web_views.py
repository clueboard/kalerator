from flask import url_for


def test_index(client):
    res = client.get(url_for('index'))
    print res
    assert res.status_code == 200
    assert 'Enter a Keyboard-Layout-Editor URL' in res.data
