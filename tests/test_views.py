#
# test_views.py
#

import pytest

from tests import client
from sys import platform

APIPATH = "/api-1.0"


def test_main(client):
    page = client.get("/")
    html = page.data.decode()

    assert """You are now being redirected to the static page <a href="https://21cmsense.netlify.app">front-end</a> on Netlify.""" in html
    assert page.status_code == 200


def test_ping(client):
    page = client.get(APIPATH + "/ping")
    html = page.data.decode()

    assert """{"pong":""}""" in html
    assert page.status_code == 200


# [
#  "location",
#  "calculation",
#  "beam",
#  "antenna"
# ]
def test_list_all_schema_groups(client):
    page = client.get(APIPATH + "/schema")
    json = page.get_json()
    assert type(json) == list
    assert page.status_code == 200


# [
#  "GaussianBeam"
# ]
def test_get_schema_group(client):
    page = client.get(APIPATH + "/schema")
    json = page.get_json()
    for group in json:
        schema_page = client.get(APIPATH + f"/schema/{group}")
        schema_json = schema_page.get_json()
        assert type(schema_json) == list
    assert page.status_code == 200


# {
#   "__comment__": "this is an extension of the JSON schema document and includes 'default' specifier",
#   "schema": "GaussianBeam",
#   "description": "GaussianBeam type beam",
#   "group": "beam",
#   "data": {
#     "beam": {
#       "class": {
#         "type": "string",
#         "help": "The beam class",
#         "default": "GaussianBeam"
#       },
# ...
def test_get_schema(client):
    page = client.get(APIPATH + "/schema/beam/get/GaussianBeam")
    json = page.get_json()
    assert json['schema'] == "GaussianBeam"
    assert page.status_code == 200


def test_get_nonexistent_schema(client):
    page = client.get(APIPATH + "/schema/beam/get/NoSuchSchema")
    assert page.status_code == 404


@pytest.mark.skipif(platform == "linux", reason="Case sensitive file will fail on linux")
def test_get_nonexistent_schema_group_case_insensitive_fs(client):
    # there is no such group as "Beam" (it is "beam")
    page = client.get(APIPATH + "/schema/Beam/get/GaussianBeam")
    assert page.status_code == 200


@pytest.mark.skipif(platform == "darwin", reason="Case sensitive file will succeed on MacOS")
def test_get_nonexistent_schema_group_case_sensitive_fs(client):
    # there is no such group as "Beam" (it is "beam")
    page = client.get(APIPATH + "/schema/Beam/get/GaussianBeam")
    assert page.status_code == 404


def test_calculation(client):
    assert True


# e.g. "calculation": "baselines-dist"  (should be "baselines-distributions)
#    {
#         "error": "unknown calculation"
#     }
def test_unknown_calculation(client):
    assert True
