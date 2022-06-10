import pytest

import app
import app.api
from app.api.models import *

# from app import api


@pytest.fixture
def client():
    testapp = app.create_app("default")
    client = testapp.test_client()

    # a = api.context()
    # get_schema_descriptions('calculation')
    yield client
