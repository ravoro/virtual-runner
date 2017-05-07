from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, Length, NumberRange, ValidationError

from .repositories import UserRepo


class JourneysAddForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    distance_meters = IntegerField(validators=[NumberRange(min=100)])
    start_lat = DecimalField(validators=[NumberRange(-90, 90)])
    start_lng = DecimalField(validators=[NumberRange(-180, 180)])
    finish_lat = DecimalField(validators=[NumberRange(-90, 90)])
    finish_lng = DecimalField(validators=[NumberRange(-180, 180)])


class JourneysAddStageForm(FlaskForm):
    distance_meters = IntegerField(validators=[NumberRange(min=100)])


class UserRegisterForm(FlaskForm):
    email = StringField(validators=[Email(), Length(max=64)])
    password = PasswordField(validators=[Length(min=8, max=64)])

    @staticmethod
    def validate_email(form, field):
        if UserRepo.get_by_email(field.data) is not None:
            raise ValidationError('"{}" is already registered. Please choose a different email.'.format(field.data))
