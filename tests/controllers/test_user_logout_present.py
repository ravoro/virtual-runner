from urllib.parse import urlparse

from . import BaseCase, common_test_require_auth


class Test(BaseCase):
    def setUp(self):
        super().setUp()

        self.valid_request = {
            'method': 'GET',
            'path': '/logout'
        }

    @common_test_require_auth
    def test_auth(self):
        pass

    def test_empty_form(self):
        """Return 302 status, redirect to / and log out the user."""
        response = self.make_request_with_auth()
        html = self.response_html(response)

        with self.test_client.session_transaction() as session:
            assert session['_flashes'][0][1] == 'Successfully logged out.'
            assert 'user_id' not in session
            assert '_id' not in session
        assert response.status_code == 302
        assert urlparse(response.headers['location']).path == '/'
