from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField
from wtforms.validators import DataRequired, NumberRange


class JourneysAddForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    start_lat = DecimalField(validators=[NumberRange(-90, 90)])
    start_lng = DecimalField(validators=[NumberRange(-180, 180)])
    finish_lat = DecimalField(validators=[NumberRange(-90, 90)])
    finish_lng = DecimalField(validators=[NumberRange(-180, 180)])
