from datetime import datetime
from unittest import TestCase

import config
from app import create_app
from app.models import db, Journey, Stage
from app.repositories import StageRepo


class TestAllOrdered(TestCase):
    """Integration tests for StageRepo.all_ordered()."""

    def setUp(self):
        def create_journey(id):
            journey = Journey(
                id=id,
                name="journey #{}".format(id),
                distance_meters=12345,
                start_lat=0.0,
                start_lng=0.0,
                finish_lat=1.0,
                finish_lng=1.0
            )
            db.session.add(journey)
            db.session.commit()
            return journey

        def create_stage(id, date, jid):
            stage = Stage(
                id=id,
                distance_meters=12345,
                date_created=date,
                journey_id=jid
            )
            db.session.add(stage)
            db.session.commit()

            if date is None:
                stage.date_created = None
                db.session.commit()

            return stage

        self.create_journey = create_journey
        self.create_stage = create_stage
        self.app = create_app(config.TestConfig)
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_no_stages(self):
        """Return empty list when no stages."""
        with self.app.app_context():
            journey = self.create_journey(1)
            assert StageRepo.all_ordered(journey.id) == []

    def test_no_stages_in_journey(self):
        """Return empty list when no stages for the provided journey (but there are stages in another journey)."""
        with self.app.app_context():
            journey1 = self.create_journey(1)
            journey2 = self.create_journey(2)
            stage2_1 = self.create_stage(1, None, journey2.id)
            stage2_2 = self.create_stage(2, None, journey2.id)
            assert StageRepo.all_ordered(journey1.id) == []

    def test_order_date_desc(self):
        """Return list of stages ordered by date in descending order."""
        with self.app.app_context():
            journey = self.create_journey(1)
            stage1 = self.create_stage(1, datetime(2016, 3, 6), journey.id)
            stage2 = self.create_stage(2, datetime(2016, 3, 7), journey.id)
            stage3 = self.create_stage(3, datetime(2016, 3, 5), journey.id)
            assert StageRepo.all_ordered(journey.id) == [stage2, stage1, stage3]

    def test_order_same_date(self):
        """Return list of stages ordered by id (descending) in cases where date is the same."""
        with self.app.app_context():
            journey = self.create_journey(1)
            stage1 = self.create_stage(1, datetime(2016, 3, 6), journey.id)
            stage2 = self.create_stage(2, datetime(2016, 3, 7), journey.id)
            stage3 = self.create_stage(3, datetime(2016, 3, 6), journey.id)
            assert StageRepo.all_ordered(journey.id) == [stage2, stage3, stage1]

    def test_order_null_after_date(self):
        """Return list of stages where stages that have a null date are ordered after stages with dates."""
        with self.app.app_context():
            journey = self.create_journey(1)
            stage1 = self.create_stage(1, datetime(2016, 3, 6), journey.id)
            stage2 = self.create_stage(2, None, journey.id)
            stage3 = self.create_stage(3, datetime(2016, 3, 5), journey.id)
            assert StageRepo.all_ordered(journey.id) == [stage1, stage3, stage2]

    def test_order_nulls(self):
        """Return list of stages where stages that have a null date are ordered by id (descending)."""
        with self.app.app_context():
            journey = self.create_journey(1)
            stage1 = self.create_stage(1, None, journey.id)
            stage2 = self.create_stage(2, datetime(2016, 3, 7), journey.id)
            stage3 = self.create_stage(3, None, journey.id)
            assert StageRepo.all_ordered(journey.id) == [stage2, stage3, stage1]
