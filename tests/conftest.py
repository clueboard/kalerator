import pytest
from kalerator.web_app import app as kalerator_app

@pytest.fixture
def app():
    return kalerator_app
