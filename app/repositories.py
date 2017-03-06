from typing import List

from app.models import db, Journey, Stage


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
    def get(id: int) -> Journey:
        return Journey.query.get(id)


class StageRepo:
    @staticmethod
    def all_ordered(jid: int) -> List[Stage]:
        return db.session \
            .query(Stage) \
            .join(Journey.stages) \
            .filter_by(journey_id=jid) \
            .order_by(Stage.id.desc(), Stage.date_created.desc()) \
            .all()

    @staticmethod
    def create(stage: Stage) -> Stage:
        db.session.add(stage)
        db.session.commit()
        return stage
