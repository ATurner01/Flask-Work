from flask_wtf import Form
from wtforms import TextField, TextAreaField, BooleanField
from wtforms.validators import DataRequired
from app import models

class TaskForm(Form):
    title = TextField("title", validators=[DataRequired()])
    desc = TextAreaField("desc")


class CompleteForm(Form):
    complete = BooleanField("complete")
    task = None
