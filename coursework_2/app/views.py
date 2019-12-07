from flask import render_template, flash, redirect, bcrypt
from flask_login import *
from app import app, db, models
from .forms import LoginForm

@login_manager.user_loader
def user_loader(user_id):
    return models.User.query.get(user_id)

@app.route('/', methods=['GET', 'POST'])
def Login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.get(form.username.data)
        if user:
            if bcrytpt.check_password_hash(user.password, form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)

                return redirect('/home')
            else:
                flash("Incorrect username or password.")
        else:
            flash("Account does not exist.")
        
    return render_template("login.html",
                           title="Login",
                           form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def Logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()

    return redirect('/')

@app.route('/home')
@login_required
def Home():
    return render_template("home.html",
                           title="Home")


