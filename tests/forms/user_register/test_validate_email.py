from unittest.mock import patch, Mock

from unittest import TestCase
from werkzeug.datastructures import MultiDict

import config
from app import create_app
from app.forms import UserRegisterForm
from app.models import User
from app.repositories import UserRepo


class Test(TestCase):
    def setUp(self):
        self.app = create_app(config.TestConfig)
        self.valid_data = MultiDict([
            ('email', 'test@example.com'),
            ('password', 'randompassword')
        ])

    @patch.object(UserRepo, 'get_by_email')
    def test_existing_email(self, mock_get_by_email: Mock):
        """Ensure form is invalid when email is already registered."""
        mock_get_by_email.return_value = User(id=1, email='test@example.com', password='samplepassword')
        with self.app.app_context():
            form = UserRegisterForm(self.valid_data)
            assert form.validate() is False

    @patch.object(UserRepo, 'get_by_email')
    def test_new_email(self, mock_get_by_email: Mock):
        """Ensure form is valid when the email is not already registered."""
        mock_get_by_email.return_value = None
        with self.app.app_context():
            form = UserRegisterForm(self.valid_data)
            assert form.validate() is True
