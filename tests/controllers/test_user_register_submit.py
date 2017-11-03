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
            'path': '/register',
            'content_type': 'application/x-www-form-urlencoded',
            'data': self.valid_data
        }

    @common_test_require_anonymous
    def test_auth(self):
        pass

    @patch.object(UserRepo, 'get_by_email_or_username')
    def test_invalid_submission(self, mock_get: Mock):
        """Return 400 status and re-present the page with UserRegisterForm errors."""
        mock_get.return_value = None
        invalid_data = self.valid_data.copy()
        invalid_data['email_or_username'] = ''
        response = self.make_request(data=invalid_data)
        html = self.response_html(response)

        assert response.status_code == 400
        assert "Please fix any errors below and try again" in html.select_one("#content form .alert").text

    @patch.object(UserRepo, 'add')
    @patch.object(UserRepo, 'get_by_email_or_username')
    def test_valid_submission(self, mock_get: Mock, mock_add: Mock):
        """Return 302 status, save user to db, and redirect to the login page when given valid submission."""
        mock_get.return_value = None
        user = self.make_user(email=self.valid_data['email_or_username'], password=self.valid_data['password'])
        mock_add.return_value = user

        response = self.make_request()

        assert mock_add.call_count is 1
        with self.test_client.session_transaction() as session:
            assert session['_flashes'][0][1] == 'Successfully registered.'
            assert session['user_id'] == str(user.id)
            assert len(session['_id']) > 0
        assert response.status_code == 302
        assert urlparse(response.headers['location']).path == '/journeys'

    @patch.object(UserRepo, 'add')
    @patch.object(UserRepo, 'get_by_email_or_username')
    def test_email_submission(self, mock_get: Mock, mock_add: Mock):
        """Ensure added record has an email and no username, when registering with an email."""
        mock_get.return_value = None
        mock_add.return_value = self.make_user()

        self.make_request()

        added_user = mock_add.call_args[0][0]
        assert added_user.email == self.valid_data['email_or_username']
        assert added_user.username is None

    @patch.object(UserRepo, 'add')
    @patch.object(UserRepo, 'get_by_email_or_username')
    def test_username_submission(self, mock_get: Mock, mock_add: Mock):
        """Ensure added record has a username and no email, when registering with a username."""
        self.valid_data['email_or_username'] = 'testuser'
        mock_get.return_value = None
        mock_add.return_value = self.make_user()

        self.make_request()

        added_user = mock_add.call_args[0][0]
        assert added_user.email is None
        assert added_user.username == self.valid_data['email_or_username']
