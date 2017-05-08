from unittest.mock import patch, Mock

from unittest import TestCase
from werkzeug.datastructures import MultiDict

import config
from app import create_app
from app.forms import UserLoginForm
from app.models import User
from app.repositories import UserRepo


class Test(TestCase):
    def setUp(self):
        self.app = create_app(config.TestConfig)
        self.valid_data = MultiDict([
            ('email_or_username', 'test@example.com'),
            ('password', 'randompassword')
        ])
        self.valid_user = User(
            id=1,
            email=self.valid_data.get('email_or_username'),
            password=self.valid_data.get('password')
        )

    @patch.object(UserRepo, 'get_by_email_or_username')
    def test_non_existing_email(self, mock_get_by_email_or_username: Mock):
        """Return False when given an unregistered email."""
        mock_get_by_email_or_username.return_value = None
        with self.app.app_context():
            form = UserLoginForm(self.valid_data)
        assert form.validate() is False
        assert form.email_or_username.errors == ['Invalid email or password.']
        assert form.password.errors == ['Invalid email or password.']

    @patch.object(UserRepo, 'get_by_email_or_username')
    def test_bad_password(self, mock_get_by_email_or_username: Mock):
        """Return False when given a wrong password."""
        mock_get_by_email_or_username.return_value = self.valid_user
        invalid_data = self.valid_data.copy()
        invalid_data.pop('password')
        invalid_data.add('password', 'wrongpassword')
        with self.app.app_context():
            form = UserLoginForm(invalid_data)
        assert form.validate() is False
        assert form.email_or_username.errors == ['Invalid email or password.']
        assert form.password.errors == ['Invalid email or password.']

    @patch.object(UserRepo, 'get_by_email_or_username')
    def test_valid_credentials(self, mock_get_by_email_or_username: Mock):
        """Return True when given valid credentials."""
        mock_get_by_email_or_username.return_value = self.valid_user
        with self.app.app_context():
            form = UserLoginForm(self.valid_data)
        assert form.validate() is True
        assert form.email_or_username.errors == []
        assert form.password.errors == []
