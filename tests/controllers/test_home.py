from urllib.parse import urlparse

from . import BaseCase


class Test(BaseCase):
    def setUp(self):
        super().setUp()

        self.valid_request = {
            'method': 'GET',
            'path': '/'
        }

    def test_authed(self):
        """Return 302 status and redirect to /journeys when user is already logged in."""
        response = self.make_request_with_auth()
        assert response.status_code == 302
        assert urlparse(response.headers['location']).path == '/journeys'

    def test_ok(self):
        """Return 200 status and display the home page."""
        response = self.make_request()
        html = self.response_html(response)
        assert response.status_code == 200
        assert 'page-home' == html.select_one("body").attrs['id']
