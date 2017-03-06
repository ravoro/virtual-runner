from urllib.parse import urlparse

from . import BaseCase


class TestHome(BaseCase):
    def setUp(self):
        super().setUp()

        self.valid_request = {
            'method': 'GET',
            'path': '/'
        }

    def test_redirect(self):
        """Return 302 status and redirect to /journeys."""
        response = self.make_request()
        assert response.status_code == 302
        assert urlparse(response.headers['location']).path == '/journeys'
