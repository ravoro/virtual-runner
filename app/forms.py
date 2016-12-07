from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField
from wtforms.validators import DataRequired, NumberRange


class JourneysAddForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    startLat = DecimalField('startLat', validators=[NumberRange(-90, 90)])
    startLng = DecimalField('startLng', validators=[NumberRange(-180, 180)])
    finishLat = DecimalField('finishLat', validators=[NumberRange(-90, 90)])
    finishLng = DecimalField('finishLng', validators=[NumberRange(-180, 180)])
