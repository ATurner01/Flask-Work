from flask import render_template, flash, redirect, request
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from passlib.hash import sha256_crypt
from datetime import date
from app import app, db, models, login_manager
from .forms import LoginForm, RegisterForm, PasswordUpdateForm

@login_manager.user_loader
def user_loader(user_id):
    """Tells flask-login how to load a user account"""

    return models.User.query.filter_by(username=user_id).first()

@login_manager.unauthorized_handler
def unauthorized():
    """Return this message and send the user to the login page
    if they are not logged in"""

    flash("You must be logged in to access this page.")
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def Login():
    """Queries the User table and attempts to log them in based on the
    provided account information"""

    form = LoginForm()

    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user:
            if sha256_crypt.verify(form.password.data, user.password):
                #Update the user's authentication status before logging in
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
    """Attempts to register a new user to the system based on the provided
    information."""

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            passHash = sha256_crypt.encrypt(form.password.data) #Hash the users password for storage in the DB
            user = models.User(username=form.username.data,password=passHash,password_last_update=date.today(),email=form.email.data)
            db.session.add(user)
            db.session.commit()
            flash("Account creation successful. You may now login.")
            return redirect('/login')
        except IntegrityError:
            #In the event the user enters a username that is already in use, rollback the current session
            #and have them try again
            db.session.rollback()
            flash("Error. Username is already in use. Please choose a different one.")

    return render_template("register.html",
                           title="Register",
                           form=form,
                           user=None)

@app.route('/update_password', methods=['GET', 'POST'])
@login_required
def UpdatePassword():
    """Updates the user password to the new password they have provided"""

    user = current_user
    form = PasswordUpdateForm()

    if form.validate_on_submit():
        if sha256_crypt.verify(form.current_password.data, user.password):
            if (form.new_password.data == form.confirm_password.data):
                newPassHash = sha256_crypt.encrypt(form.new_password.data)
                user.password = newPassHash
                user.password_last_update = date.today()
                db.session.add(user)
                db.session.commit()
                flash("Password updated successfully.")
                return redirect('/account')
            else:
                flash("You must confirm your password by entering the same password twice.")
        else:
            flash("Your current password is incorrect.")

    return render_template("update_password.html",
                           title="Update Password",
                           user=user,
                           form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def Logout():
    """Logout the current user (if there is a user currently logged in)"""

    user = current_user
    user.authenticated = False #Update the state of the user to make them unauthorised
    db.session.add(user)
    db.session.commit()
    logout_user() #Calls flask-login's logout function to ensure session is correctly terminated

    return redirect('/')

@app.route('/')
def Home():
    """Displays the Homepage of the website to the user"""

    user = current_user
    return render_template("home.html",
                           title="Home",
                           user=user)

@app.route('/account')
@login_required
def Account():
    """Show the user their account information if they are logged in"""

    user = current_user
    return render_template("account.html",
                           title="Account",
                           user=user)


@app.route('/list_books')
def ListBooks():
    user = current_user
    books = models.Book.query.all()

    return render_template("list_books.html",
                            title="List Books",
                            user=user,
                            books=books)

@app.route('/details', methods=['GET', 'POST'])
def Details():
    user = current_user
    id = request.form.getlist('id')
    book = models.Book.query.get(id[0])

    return render_template("details.html",
                           title=book.title,
                           user=user,
                           book=book)


