#
# test_schema.py
#

from app.schema import *
import pytest

from app import create_app
import app

from tests import client


def test_get_schema_descriptions():
    assert True
    testapp = app.create_app('default')

    # ret=client.get("/api-1.0/schema/calculation/descriptions")

    # a = app.context()
    # with testapp.test_request_context('/21cm/schema'):
    #
    #     thejson = get_schema_descriptions_json('calculation')
    #     assert not thejson
    #
    #     thejson = get_schema_descriptions_json('calculations')
    #     assert thejson
