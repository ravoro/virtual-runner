from unittest.mock import patch, Mock
from urllib.parse import urlparse

from app.repositories import UserRepo
from . import BaseCase, common_test_require_anonymous


class Test(BaseCase):
    def setUp(self):
        super().setUp()

        self.valid_data = {
            'email_or_username': 'test@example.com',
            'password': 'samplepassword'
        }

        self.valid_request = {
            'method': 'POST',
            'path': '/login',
            'content_type': 'application/x-www-form-urlencoded',
            'data': self.valid_data
        }

    @common_test_require_anonymous
    def test_auth(self):
        pass

    @patch.object(UserRepo, 'get_by_email_or_username')
    def test_invalid_submission(self, mock_get_by_email_or_username: Mock):
        """Return 400 status and re-present the page with UserLoginForm errors."""
        mock_get_by_email_or_username.return_value = None
        invalid_data = self.valid_data.copy()
        invalid_data['email_or_username'] = ''
        response = self.make_request(data=invalid_data)
        html = self.response_html(response)

        assert response.status_code == 400
        assert "Please fix any errors below and try again" in html.select_one("#content form .alert").text

    @patch.object(UserRepo, 'get_by_email_or_username')
    def test_valid_submission(self, mock_get_by_email_or_username: Mock):
        """Return 302 status, create a session and redirect to the journeys page when given valid submission."""
        user = self.make_user(email=self.valid_data['email_or_username'], password=self.valid_data['password'])
        mock_get_by_email_or_username.return_value = user

        response = self.make_request()

        with self.test_client.session_transaction() as session:
            assert session['_flashes'][0][1] == 'Successfully logged in.'
            assert session['user_id'] == str(user.id)
            assert len(session['_id']) > 0
        assert response.status_code == 302
        assert urlparse(response.headers['location']).path == '/journeys'
