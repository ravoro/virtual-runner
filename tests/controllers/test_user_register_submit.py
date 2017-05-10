from unittest.mock import patch, Mock
from urllib.parse import urlparse

from app.repositories import UserRepo
from . import BaseCase, common_test_require_anonymous


class Test(BaseCase):
    def setUp(self):
        super().setUp()

        self.valid_data = {
            'email': 'test@example.com',
            'password': 'samplepassword'
        }

        self.valid_request = {
            'method': 'POST',
            'path': '/register',
            'content_type': 'application/x-www-form-urlencoded',
            'data': self.valid_data
        }

    @common_test_require_anonymous
    def test_auth(self):
        pass

    @patch.object(UserRepo, 'get_by_email')
    def test_invalid_submission(self, mock_get_by_email: Mock):
        """Return 400 status and re-present the page with UserRegisterForm errors."""
        mock_get_by_email.return_value = None
        invalid_data = self.valid_data.copy()
        invalid_data['email'] = ''
        response = self.make_request(data=invalid_data)
        html = self.response_html(response)

        assert response.status_code == 400
        assert "Please fix any errors below and try again" in html.select_one("#content form .alert").text

    @patch.object(UserRepo, 'add')
    @patch.object(UserRepo, 'get_by_email')
    def test_valid_submission(self, mock_get_by_email: Mock, mock_add: Mock):
        """Return 302 status, save user to db, and redirect to the login page when given valid submission."""
        mock_get_by_email.return_value = None
        user = self.make_user(**self.valid_data)
        mock_add.return_value = user

        response = self.make_request()

        assert mock_add.call_count is 1
        with self.test_client.session_transaction() as session:
            assert session['_flashes'][0][1] == 'Successfully registered.'
        assert response.status_code == 302
        assert urlparse(response.headers['location']).path == '/login'
