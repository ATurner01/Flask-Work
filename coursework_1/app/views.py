from flask import render_template, flash, request, redirect
from app import app, db, models
from .forms import TaskForm, CompleteForm
import datetime


@app.route('/', methods=['GET', 'POST'])
def display_tasks():
    tasks = models.Task.query.all()
    form = CompleteForm()

    if form.validate_on_submit():
        models.Task.query,get(1).completed = True
        db.session.commit()

    return render_template("view_tasks.html",
                           title="Tasks",
                           tasks=tasks,
                           form=form)

@app.route('/completed')
def display_completed():
    tasks = models.Task.query.all()
    
    return render_template("view_completed.html",
                           title="Completed Tasks",
                           tasks=tasks)

@app.route('/add_task', methods=['GET', 'POST'])
def create_task():
    form = TaskForm()

    if form.validate_on_submit():
        flash("Succesfully received form data.")

        task = models.Task(title=form.title.data, description=form.desc.data, date=datetime.date.today(), completed=False)
        db.session.add(task)
        db.session.commit()


    return render_template("create_task.html",
                           title="Create New Task.",
                           form=form)

@app.route('/update', methods=['GET', 'POST'])
def update_record():
    id = request.form.getlist('id')
    models.Task.query.get(id[0]).completed = True
    db.session.commit()

    return redirect('/')
