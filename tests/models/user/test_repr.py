from unittest import TestCase

from app.models import User


class Test(TestCase):
    def test_correct_repr(self):
        """Return string representing the user object."""
        user = User(
            id=543,
            email='test@example.com',
            password='randompassword'
        )
        assert user.__repr__() == "<User id={}>".format(user.id)
