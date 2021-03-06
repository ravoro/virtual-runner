from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import DecimalField, IntegerField, PasswordField, StringField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError

from .repositories import UserRepo


class JourneysAddForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    distance_meters = IntegerField(validators=[NumberRange(min=100)])
    start_lat = DecimalField(validators=[NumberRange(-90, 90)])
    start_lng = DecimalField(validators=[NumberRange(-180, 180)])
    finish_lat = DecimalField(validators=[NumberRange(-90, 90)])
    finish_lng = DecimalField(validators=[NumberRange(-180, 180)])


class JourneyAddStageForm(FlaskForm):
    distance_meters = IntegerField(validators=[NumberRange(min=100)])


class BaseAuthForm(FlaskForm):
    email_or_username = StringField(validators=[Length(min=2, max=64)])
    password = PasswordField(validators=[Length(min=8, max=64)])


class UserLoginForm(BaseAuthForm):
    def validate(self):
        return super().validate() and self._validate_credentials()

    def _validate_credentials(self):
        user = UserRepo.get_by_email_or_username(self.email_or_username.data)
        if user and check_password_hash(user._password_hash, self.password.data):
            return True
        self.email_or_username.errors = self.password.errors = ['Invalid email or password.']
        return False


class UserRegisterForm(BaseAuthForm):
    @staticmethod
    def validate_email_or_username(form, field):
        if UserRepo.get_by_email_or_username(field.data) is not None:
            raise ValidationError(
                '"{}" is already registered. Please choose a different email or username.'.format(field.data))
