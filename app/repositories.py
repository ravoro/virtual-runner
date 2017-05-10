from typing import List, Optional

from sqlalchemy import func

from app.models import db, Journey, Stage, User


class JourneyRepo:
    @staticmethod
    def all_ordered(user_id: int) -> List[Journey]:
        return Journey.query \
            .filter_by(user_id=user_id) \
            .order_by(Journey.date_created.desc(), Journey.id.desc()) \
            .all()

    @staticmethod
    def create(journey: Journey) -> Journey:
        db.session.add(journey)
        db.session.commit()
        return journey

    @staticmethod
    def get(user_id: int, journey_id: int) -> Optional[Journey]:
        return Journey.query \
            .filter_by(id=journey_id, user_id=user_id) \
            .one_or_none()


class StageRepo:
    @staticmethod
    def all_ordered(journey_id: int) -> List[Stage]:
        return db.session \
            .query(Stage) \
            .join(Journey.stages) \
            .filter_by(journey_id=journey_id) \
            .order_by(Stage.date_created.desc(), Stage.id.desc()) \
            .all()

    @staticmethod
    def create(stage: Stage) -> Stage:
        db.session.add(stage)
        db.session.commit()
        return stage

    @staticmethod
    def total_distance(user_id: int) -> int:
        """Total sum of all stage distances for the given user."""
        journeys_subquery = db.session \
            .query(Journey.id) \
            .join(User) \
            .filter(User.id == user_id) \
            .subquery()
        distance_sum = db.session \
            .query(func.sum(Stage.distance_meters)) \
            .filter(Stage.journey_id.in_(journeys_subquery)) \
            .scalar()
        return int(distance_sum) if distance_sum else 0


class UserRepo:
    @staticmethod
    def get(user_id: int) -> Optional[User]:
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_by_email_or_username(email_or_username: str) -> Optional[User]:
        return UserRepo.get_by_email(email_or_username) or \
               UserRepo.get_by_username(email_or_username)

    @staticmethod
    def add(user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user
