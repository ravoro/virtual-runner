import datetime

from flask_login import UserMixin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import FLOAT
from werkzeug.security import generate_password_hash

db = SQLAlchemy()
migrate = Migrate()


class Journey(db.Model):
    __tablename__ = 'journeys'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    distance_meters = db.Column(db.Integer, nullable=False)
    start_lat = db.Column(FLOAT(10, 6), nullable=False)
    start_lng = db.Column(FLOAT(10, 6), nullable=False)
    finish_lat = db.Column(FLOAT(10, 6), nullable=False)
    finish_lng = db.Column(FLOAT(10, 6), nullable=False)
    date_created = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now)
    stages = db.relationship('Stage', backref='journeys')

    @property
    def completed_distance(self) -> int:
        return sum([s.distance_meters for s in self.stages])

    @property
    def is_completed(self) -> bool:
        return self.completed_distance >= self.distance_meters

    @property
    def completed_fraction(self) -> float:
        if self.is_completed:
            return 1
        return self.completed_distance / self.distance_meters

    def __repr__(self) -> str:
        return '<Journey id={}>'.format(self.id)


class Stage(db.Model):
    __tablename__ = 'stages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    journey_id = db.Column(db.Integer, db.ForeignKey('journeys.id'), nullable=False)
    distance_meters = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now)

    def __repr__(self) -> str:
        return '<Stage id={}>'.format(self.id)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), unique=True, nullable=True)
    username = db.Column(db.String(64), unique=True, nullable=True)
    _password_hash = db.Column('password_hash', db.String(128), nullable=False)

    @property
    def password(self):
        raise AttributeError('attribute \'password\' is not readable')

    @password.setter
    def password(self, val):
        self._password_hash = generate_password_hash(val)

    def __repr__(self) -> str:
        return '<User id={}>'.format(self.id)
