from unittest import TestCase

from app.models import Stage


class Test(TestCase):
    def test_correct_repr(self):
        """Return string representing the stage object."""
        stage = Stage(
            id=543,
            distance_meters=12345
        )
        assert stage.__repr__() == "<Stage id={}>".format(stage.id)
