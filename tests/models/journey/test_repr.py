from unittest import TestCase

from app.models import Journey


class Test(TestCase):
    def test_correct_repr(self):
        """Return string representing the journey object."""
        journey = Journey(
            id=543,
            name="random journey name",
            distance_meters=12345,
            start_lat=0.0,
            start_lng=0.0,
            finish_lat=1.0,
            finish_lng=1.0
        )
        assert journey.__repr__() == "<Journey id={}>".format(journey.id)
