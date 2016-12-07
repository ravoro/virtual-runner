from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField
from wtforms.validators import DataRequired, NumberRange


class JourneysAddForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    startLat = DecimalField(validators=[NumberRange(-90, 90)])
    startLng = DecimalField(validators=[NumberRange(-180, 180)])
    finishLat = DecimalField(validators=[NumberRange(-90, 90)])
    finishLng = DecimalField(validators=[NumberRange(-180, 180)])
