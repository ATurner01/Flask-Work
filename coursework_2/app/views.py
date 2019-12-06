from flask import render_template, flash
from app import app
from .forms import LoginForm

@app.route('/', methods=['GET', 'POST'])
def Login():
    form = LoginForm()
    return render_template("login.html",
                           title="Login",
                           form=form)

