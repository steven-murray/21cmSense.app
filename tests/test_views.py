from tests import client

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
def test_schema_group_list(client):
    page = client.get(APIPATH + "/schema")
    json = page.get_json()
    assert type(json) == list


# [
#  "GaussianBeam"
# ]
def test_schema_list_for_each_group(client):
    page = client.get(APIPATH + "/schema")
    json = page.get_json()
    for group in json:
        schema_page = client.get(APIPATH + f"/schema/{group}")
        schema_json = schema_page.get_json()
        assert type(schema_json) == list
