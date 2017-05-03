from unittest import TestCase

from app.models import Journey, Stage


class Test(TestCase):
    def setUp(self):
        self.journey = Journey(
            id=1,
            name="random journey name",
            distance_meters=12345,
            start_lat=0.0,
            start_lng=0.0,
            finish_lat=1.0,
            finish_lng=1.0
        )

    def test_no_stages(self):
        """Return False when there are no stages."""
        self.journey.stages = []
        assert self.journey.is_completed is False

    def test_not_completed(self):
        """Return False when there are stages, but not completed."""
        incomplete_distance = self.journey.distance_meters - 1
        stage = Stage(id=1, distance_meters=incomplete_distance, journey_id=self.journey.id)
        self.journey.stages = [stage]
        assert self.journey.is_completed is False

    def test_completed(self):
        """Return True when the stages distances add up exactly to the journey distance."""
        exact_distance = self.journey.distance_meters
        stage = Stage(id=1, distance_meters=exact_distance, journey_id=self.journey.id)
        self.journey.stages = [stage]
        assert self.journey.is_completed is True

    def test_completed_extra(self):
        """Return True when the stages distances are more than the journey distance."""
        extra_distance = self.journey.distance_meters + 1
        stage = Stage(id=1, distance_meters=extra_distance, journey_id=self.journey.id)
        self.journey.stages = [stage]
        assert self.journey.is_completed is True
