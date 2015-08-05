# coding=UTF-8
import pytest
from kalerator.web.app import app as kalerator_app

@pytest.fixture
def app():
    return kalerator_app
