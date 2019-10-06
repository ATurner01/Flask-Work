from flask_wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import DataRequired

class TaskForm(Form):
    title = TextField("title", validators=[DataRequired()])
    desc = TextAreaField("desc")
