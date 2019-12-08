from flask import render_template, flash, redirect
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from passlib.hash import sha256_crypt
from app import app, db, models, login_manager
from .forms import LoginForm, RegisterForm

@login_manager.user_loader
def user_loader(user_id):
    return models.User.query.filter_by(username=user_id).first()

@login_manager.unauthorized_handler
def unauthorized():
    flash("You must be logged in to access this page.")
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginForm()

    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user:
            if sha256_crypt.verify(form.password.data, user.password):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect('/')
            else:
                flash("Incorrect username or password.")
        else:
            flash("Account does not exist.")
        
    return render_template("login.html",
                           title="Login",
                           form=form,
                           user=None)

@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            passHash = sha256_crypt.encrypt(form.password.data)
            user = models.User(username=form.username.data,password=passHash,email=form.email.data)
            db.session.add(user)
            db.session.commit()
            flash("Account creation successful. You may now login.")
            return redirect('/login')
        except IntegrityError:
            db.session.rollback()
            flash("Error. Username is already in use. Please choose a different one.")

    return render_template("register.html",
                           title="Register",
                           form=form,
                           user=None)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def Logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()

    return redirect('/')

@app.route('/')
def Home():
    user = current_user
    return render_template("home.html",
                           title="Home",
                           user=user)

@app.route('/account')
@login_required
def Account():
    user = current_user
    return render_template("account.html",
                           title="Account",
                           user=user)

