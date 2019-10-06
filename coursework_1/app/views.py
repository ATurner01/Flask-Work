from flask import render_template, flash
from app import app
from .forms import TaskForm


@app.route('/')
def index():
    return render_template("view_tasks.html",
                           title="Sample Page")

@app.route('/completed')
def display_completed():
    return render_template("view_completed.html",
                           title="Completed Tasks")

@app.route('/add_task', methods=['GET', 'POST'])
def create_task():
    form = TaskForm()
    return render_template("create_task.html",
                           title="Create New Task.",
                           form=form)




