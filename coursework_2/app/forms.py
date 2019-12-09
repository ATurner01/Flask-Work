from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = TextField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class RegisterForm(Form):
    username = TextField('username', validators=[DataRequired()])
    password = TextField('password', validators=[DataRequired()])
    email = TextField('password', validators=[DataRequired()])


class PasswordUpdateForm(Form):
    current_password = PasswordField('current_password', validators=[DataRequired()])
    new_password = PasswordField('new_password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired()])
    
    


    
