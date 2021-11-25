from tests import client


def test_main(client):
    landing = client.get("/")
    html = landing.data.decode()
    assert "<a href=\"/about/\">About</a>" in html
    assert landing.status_code == 200
