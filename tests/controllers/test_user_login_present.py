from urllib.parse import urlparse

from . import BaseCase


class Test(BaseCase):
    def setUp(self):
        super().setUp()

        self.valid_request = {
            'method': 'GET',
            'path': '/login'
        }

    def test_authed(self):
        """Return 302 status and redirect to /journeys when user is already logged in."""
        response = self.make_request_with_auth()
        assert response.status_code == 302
        assert urlparse(response.headers['location']).path == '/journeys'

    def test_empty_form(self):
        """Return 200 status and present an empty UserLoginForm."""
        response = self.make_request()
        html = self.response_html(response)

        assert response.status_code == 200
        assert html.select_one("#content form input[name=email_or_username]").attrs['value'] is ''
        assert html.select_one("#content form input[name=password]").attrs['value'] is ''
