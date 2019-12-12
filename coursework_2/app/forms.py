from flask_wtf import Form
from wtforms import TextField, PasswordField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Email, Length


class LoginForm(Form):
    username = TextField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class RegisterForm(Form):
    username = TextField('username', validators=[DataRequired()])
    password = TextField('password', validators=[DataRequired()])
    email = TextField('password', validators=[DataRequired(), Email(message="Invalid Email Address")])


class PasswordUpdateForm(Form):
    current_password = PasswordField('current_password', validators=[DataRequired()])
    new_password = PasswordField('new_password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired()])


class ReviewForm(Form):
    rating = IntegerField('rating', validators=[DataRequired(), NumberRange(min=0, max=10)])
    message = TextField('message', validators=[Length(min=0, max=500)])


