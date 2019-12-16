from flask import render_template, flash, redirect, request
from flask_login import login_required, login_user, logout_user, current_user
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from passlib.hash import sha256_crypt
from datetime import date
import json
import logging
from app import app, db, models, login_manager, api
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
    app.logger.error('Unauthorised page access attempted.')
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
                app.logger.info("Login attempt successful for " + user.username + ".") 
                return redirect('/')
            else:
                app.logger.error("Unauthorised account access attempted for " + user.username + ".")
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
            app.logger.info("Created account " + user.username + ".")
            return redirect('/login')
        except IntegrityError:
            #In the event the user enters a username that is already in use, rollback the current session
            #and have them try again
            db.session.rollback()
            flash("Error. Username is already in use. Please choose a different one.")
            app.logger.error("Attempted to create new account with an existing username.")

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
                app.logger.info("Successfully changed password for " + user.username + ".")
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
    name = user.username
    user.authenticated = False #Update the state of the user to make them unauthorised
    db.session.add(user)
    db.session.commit()
    logout_user() #Calls flask-login's logout function to ensure session is correctly terminated
    app.logger.info("Successfully logged out " + name + ".")

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
    """Lists all the current books stored in the database"""
    
    user = current_user
    books = models.Book.query.all()

    return render_template("list_books.html",
                            title="List Books",
                            user=user,
                            books=books)

@app.route('/details', methods=['GET', 'POST'])
def Details():
    """Lists the specific details of a given book"""
    
    user = current_user
    #The ID for a given book is provided through a HTML form, therefore we need to request that ID from the form
    id = request.form.getlist('id')
    #Queries the Book table to get the book relating to the provided ID from the form
    book = models.Book.query.get(id[0])

    return render_template("details.html",
                           title=book.title,
                           user=user,
                           book=book)

@app.route('/collection')
@login_required
def Collection():
    """Lists all the books that the user currently owns"""
    
    user = current_user
    #First, we need to query our helper table to find all the books this specific user owns
    owned_books = db.session.query(models.owns).filter_by(user_id=user.id).all()
    #Next, we find all the books the user owns from the Book table
    books = []
    for i in range(0, len(owned_books)):
        books.append(models.Book.query.get(owned_books[i][1])) #owned_books is a 2D array, where [i][0] is the User ID and [i][1] is the Book ID

    return render_template("collection.html",
                           title="Collection",
                           user=user,
                           books=books)

@app.route('/add_book', methods=['POST'])
@login_required
def AddBook():
    """Allows a user to add a book to their personal collection"""

    #Retrieve the data from the AJAX request and parse the data as an integer
    data = json.loads(request.data)
    book_id = int(data.get('book_id'))

    #Look iup both the current user and the book that was selected
    user = current_user
    book = models.Book.query.get(book_id)
    user = models.User.query.get(user.id)
    #Attepts to add the selected book to the users list of owned books. Incase an error occurs (we try to add 2 of the same book), rollback the database and abort commit
    try:
        user.owns.append(book)
        db.session.add(user)
        db.session.commit()
        app.logger.info("Added book to " + user.username + "'s collection.")
    except IntegrityError:
        db.session.rollback()
        

    return json.dumps({'status': 'OK', 'book_id': book_id})
