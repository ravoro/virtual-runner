from unittest.mock import patch, Mock

from unittest import TestCase
from werkzeug.datastructures import MultiDict
from wtforms import ValidationError

import config
from app import create_app
from app.forms import UserRegisterForm
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
            username=None,
            password=self.valid_data.get('password')
        )

    @patch.object(UserRepo, 'get_by_email_or_username')
    def test_existing_value(self, mock_get: Mock):
        """Raise ValidationError when value is already registered."""
        mock_get.return_value = self.valid_user
        with self.app.app_context():
            form = UserRegisterForm(self.valid_data)
        with self.assertRaises(ValidationError):
            form.validate_email_or_username(form, form.email_or_username)

    @patch.object(UserRepo, 'get_by_email_or_username')
    def test_new_value(self, mock_get: Mock):
        """Do not raise ValidationError when the value is not registered."""
        mock_get.return_value = None
        with self.app.app_context():
            form = UserRegisterForm(self.valid_data)
        try:
            res = form.validate_email_or_username(form, form.email_or_username)
            assert res is None
        except ValidationError:
            self.fail('ValidationError should not be raised')
