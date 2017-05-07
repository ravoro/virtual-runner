from unittest import TestCase
from werkzeug.security import check_password_hash

from app.models import User


class Test(TestCase):
    def setUp(self):
        self.valid_data = {
            'id': 543,
            'email': 'test@example.com',
            'password': 'randompassword'
        }

    def test_cannot_read_password(self):
        """Raise AttributeError when trying to read the password attribute."""
        user = User(**self.valid_data)
        with self.assertRaises(AttributeError):
            user.password

    def test_password_hashed(self):
        """Ensure password is hashed when saved."""
        user = User(**self.valid_data)
        assert user._password_hash != self.valid_data['password']
        assert check_password_hash(user._password_hash, self.valid_data['password'])
