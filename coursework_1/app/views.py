from flask import render_template
from app import app


@app.route('/')
def index():
    return render_template("view_tasks.html",
                           title="Sample Page")

@app.route('/completed')
def display_completed():
    return render_template("view_completed.html",
                           title="Completed Tasks")

@app.route('/add_task')
def create_task():
    return render_template("create_task.html",
                           title="Create New Task.")


