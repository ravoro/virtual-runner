from app import db


class Journey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    start_lat = db.Column(db.Float)
    start_lng = db.Column(db.Float)
    finish_lat = db.Column(db.Float)
    finish_lng = db.Column(db.Float)

    def __init__(self, name, start_lat, start_lng, finish_lat, finish_lng):
        self.name = name
        self.start_lat = start_lat
        self.start_lng = start_lng
        self.finish_lat = finish_lat
        self.finish_lng = finish_lng

    def __repr__(self):
        return '<User {} | {} | ({}, {}) | ({}, {})>'.format(
            self.id, self.name, self.start_lat, self.start_lng, self.finish_lat, self.finish_lng)
