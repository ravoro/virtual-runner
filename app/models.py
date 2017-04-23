import datetime

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


class Journey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    distance_meters = db.Column(db.Integer)
    start_lat = db.Column(db.Float)
    start_lng = db.Column(db.Float)
    finish_lat = db.Column(db.Float)
    finish_lng = db.Column(db.Float)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)
    stages = db.relationship('Stage', backref='journey')

    @property
    def completed_distance(self) -> int:
        return sum([s.distance_meters for s in self.stages])

    @property
    def is_completed(self) -> bool:
        return self.completed_distance >= self.distance_meters

    def __repr__(self) -> str:
        return '<Journey id={}>'.format(self.id)


class Stage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    distance_meters = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)
    journey_id = db.Column(db.Integer, db.ForeignKey('journey.id'))

    def __repr__(self) -> str:
        return '<Stage id={}>'.format(self.id)
