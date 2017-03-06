from unittest import TestCase

from app.models import Journey, Stage


class TestCompletedDistance(TestCase):
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
        """Return 0 when there are no stages."""
        self.journey.stages = []
        assert self.journey.completed_distance == 0

    def test_correct_sum(self):
        """Return sum of stage distances."""
        stage1 = Stage(id=1, distance_meters=5200, journey_id=self.journey.id)
        stage2 = Stage(id=2, distance_meters=3656, journey_id=self.journey.id)
        self.journey.stages = [stage1, stage2]
        assert self.journey.completed_distance == stage1.distance_meters + stage2.distance_meters
