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
        """Return 0 when there are no stages."""
        self.journey.stages = []
        assert self.journey.completed_fraction == 0

    def test_stages_completed(self):
        """Return 1 when journey completed."""
        final_stage = Stage(id=1, distance_meters=self.journey.distance_meters, journey_id=self.journey.id)
        self.journey.stages = [final_stage]
        assert self.journey.completed_fraction == 1

    def test_stages_completed_extra(self):
        """Return 1 when journey completed with extra distance."""
        final_stage = Stage(id=1, distance_meters=self.journey.distance_meters + 1, journey_id=self.journey.id)
        self.journey.stages = [final_stage]
        assert self.journey.completed_fraction == 1

    def test_correct_sum(self):
        """Return fraction of the entire journey completed."""
        stage1 = Stage(id=1, distance_meters=5200, journey_id=self.journey.id)
        stage2 = Stage(id=2, distance_meters=3656, journey_id=self.journey.id)
        self.journey.stages = [stage1, stage2]
        fraction = (stage1.distance_meters + stage2.distance_meters) / self.journey.distance_meters
        assert self.journey.completed_fraction == fraction
