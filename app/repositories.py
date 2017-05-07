from sqlalchemy import func
from typing import List, Optional

from app.models import db, Journey, Stage, User


class JourneyRepo:
    @staticmethod
    def all_ordered() -> List[Journey]:
        return Journey.query \
            .order_by(Journey.date_created.desc(), Journey.id.desc()) \
            .all()

    @staticmethod
    def create(journey: Journey) -> Journey:
        db.session.add(journey)
        db.session.commit()
        return journey

    @staticmethod
    def get(id: int) -> Optional[Journey]:
        return Journey.query.get(id)


class StageRepo:
    @staticmethod
    def all_ordered(jid: int) -> List[Stage]:
        return db.session \
            .query(Stage) \
            .join(Journey.stages) \
            .filter_by(journey_id=jid) \
            .order_by(Stage.date_created.desc(), Stage.id.desc()) \
            .all()

    @staticmethod
    def create(stage: Stage) -> Stage:
        db.session.add(stage)
        db.session.commit()
        return stage

    @staticmethod
    def total_distance() -> int:
        """Total sum of all stage distances."""
        return db.session \
            .query(func.sum(Stage.distance_meters)) \
            .scalar()


class UserRepo:
    @staticmethod
    def get(user_id: int) -> Optional[User]:
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        return User.query.filter_by(email=email).first()

    @staticmethod
    def add(user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user
