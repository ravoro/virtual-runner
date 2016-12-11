from app import db


class Journey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    start_lat = db.Column(db.Float)
    start_lng = db.Column(db.Float)
    finish_lat = db.Column(db.Float)
    finish_lng = db.Column(db.Float)
    stages = db.relationship('Stage', backref='journey')

    @property
    def stages_to_distances(self):
        return [s.distance for s in self.stages]

    def __repr__(self):
        return '<Journey id={}>'.format(self.id)


class Stage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    distance = db.Column(db.Integer)
    journey_id = db.Column(db.Integer, db.ForeignKey('journey.id'))

    def __repr__(self):
        return '<Stage id={}>'.format(self.id)
