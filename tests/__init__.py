import app.api
import app
from app.api.models import *
import pytest
#from app import api


@pytest.fixture
def client():
    a=app.create_app('')

    # a = api.context()
    # get_schema_descriptions('calculation')
    yield a


