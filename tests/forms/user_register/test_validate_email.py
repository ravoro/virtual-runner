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
            ('email', 'test@example.com'),
            ('password', 'randompassword')
        ])

    @patch.object(UserRepo, 'get_by_email')
    def test_existing_email(self, mock_get_by_email: Mock):
        """Raise ValidationError when email is already registered."""
        mock_get_by_email.return_value = User(id=1, **self.valid_data.to_dict())
        with self.app.app_context():
            form = UserRegisterForm(self.valid_data)
        with self.assertRaises(ValidationError):
            form.validate_email(form, form.email)

    @patch.object(UserRepo, 'get_by_email')
    def test_new_email(self, mock_get_by_email: Mock):
        """Do not raise ValidationError when the email is not registered."""
        mock_get_by_email.return_value = None
        with self.app.app_context():
            form = UserRegisterForm(self.valid_data)
        try:
            res = form.validate_email(form, form.email)
            assert res is None
        except ValidationError:
            self.fail('ValidationError should not be raised')
