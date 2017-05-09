from datetime import datetime
from unittest import TestCase

import config
from app import create_app
from app.models import db, Journey, User
from app.repositories import JourneyRepo


class TestAllOrdered(TestCase):
    """Integration tests for JourneyRepo.all_ordered()."""

    def setUp(self):
        def create_journey(journey_id=1, user_id=1, date=None):
            journey = Journey(
                id=journey_id,
                user_id=user_id,
                name="journey #{}".format(id),
                distance_meters=12345,
                start_lat=0.0,
                start_lng=0.0,
                finish_lat=1.0,
                finish_lng=1.0,
                date_created=date
            )
            db.session.add(journey)
            db.session.commit()

            if date is None:
                journey.date_created = None
                db.session.commit()

            return journey

        self.create_journey = create_journey
        self.app = create_app(config.TestConfig)
        with self.app.app_context():
            db.create_all()
            user1 = User(id=1, email='test@example.com', password='samplepassword')
            user2 = User(id=2, email='another@example.com', password='anotherpassword')
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_no_journeys(self):
        """Return empty list when no journeys."""
        with self.app.app_context():
            assert JourneyRepo.all_ordered(user_id=1) == []

    def test_journeys_by_user(self):
        """Return list of journeys only belonging to the specified user."""
        with self.app.app_context():
            journey1 = self.create_journey(journey_id=1, user_id=1)
            journey2 = self.create_journey(journey_id=2, user_id=2)
            assert JourneyRepo.all_ordered(user_id=1) == [journey1]
            assert JourneyRepo.all_ordered(user_id=2) == [journey2]

    def test_order_date_desc(self):
        """Return list of journeys ordered by date in descending order."""
        with self.app.app_context():
            journey1 = self.create_journey(journey_id=1, date=datetime(2016, 3, 6))
            journey2 = self.create_journey(journey_id=2, date=datetime(2016, 3, 7))
            journey3 = self.create_journey(journey_id=3, date=datetime(2016, 3, 5))
            assert JourneyRepo.all_ordered(user_id=1) == [journey2, journey1, journey3]

    def test_order_same_date(self):
        """Return list of journeys ordered by id (descending) in cases where date is the same."""
        with self.app.app_context():
            journey1 = self.create_journey(journey_id=1, date=datetime(2016, 3, 6))
            journey2 = self.create_journey(journey_id=2, date=datetime(2016, 3, 7))
            journey3 = self.create_journey(journey_id=3, date=datetime(2016, 3, 6))
            assert JourneyRepo.all_ordered(user_id=1) == [journey2, journey3, journey1]

    def test_order_null_after_date(self):
        """Return list of journeys where journeys that have a null date are ordered after journeys with dates."""
        with self.app.app_context():
            journey1 = self.create_journey(journey_id=1, date=datetime(2016, 3, 6))
            journey2 = self.create_journey(journey_id=2, date=None)
            journey3 = self.create_journey(journey_id=3, date=datetime(2016, 3, 5))
            assert JourneyRepo.all_ordered(user_id=1) == [journey1, journey3, journey2]

    def test_order_nulls(self):
        """Return list of journeys where journeys that have a null date are ordered by id (descending)."""
        with self.app.app_context():
            journey1 = self.create_journey(journey_id=1, date=None)
            journey2 = self.create_journey(journey_id=2, date=datetime(2016, 3, 7))
            journey3 = self.create_journey(journey_id=3, date=None)
            assert JourneyRepo.all_ordered(user_id=1) == [journey2, journey3, journey1]
