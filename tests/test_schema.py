from app.schema import *
import pytest

from app import create_app
import app

from tests import client


def test_get_schema_descriptions():
    testapp = app.create_app('default')

    # a = app.context()
    with testapp.test_request_context('/21cm/schema'):
        thejson = get_schema_descriptions_json('calculation')
        assert not thejson

        thejson = get_schema_descriptions_json('calculations')
        assert thejson
