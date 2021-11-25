import app.api
import app
from app.api.models import *
import pytest


# from app import api


@pytest.fixture
def client():
    testapp = app.create_app('default')
    client = testapp.test_client()

    # a = api.context()
    # get_schema_descriptions('calculation')
    yield client
