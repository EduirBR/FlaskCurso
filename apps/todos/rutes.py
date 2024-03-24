from flask import Blueprint, render_template, request, url_for, redirect, flash, session, g
from apps.auth.services import login_required
from .models import TodoModel
from core import db

bp = Blueprint('todo', __name__, url_prefix='/todo')


@bp.route('/list', methods=['GET'])
@login_required
def index():
    todos = TodoModel.query.filter_by(created_by=g.user.id).all()
    return render_template('todo/index.html', todos=todos)

@bp.route('/', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        error = None
        if not title:
            error = 'Title is required'
        if title and TodoModel.query.filter_by(title=title, created_by=g.user.id).first() is not None:
            error = f'Todo {title} is already created'
        if error is None:
            todo = TodoModel(g.user.id, title, desc)
            db.session.add(todo)
            db.session.commit()
            return redirect(url_for('todo.index'))
        flash(error)
    
    return render_template('todo/create.html')

def get_todo(id):
    todo = TodoModel.query.filter_by(id=id, created_by=g.user.id).first()
    return todo

@bp.route('/<uuid:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    todo = get_todo(id)
    if request.method == 'POST':
        error = None
        if not request.form['title']:
            error = 'Title is required'
        if request.form['title'] and request.form['title'] != todo.title:
            if TodoModel.query.filter_by(title=request.form['title'], created_by=g.user.id).first() is not None:
                error = f'Todo {request.form["title"]} is already created'
            todo.title = request.form['title']
        if error is None:
            todo.desc = request.form['desc']
            todo.status = True if request.form.get('status') == 'on' else False
            db.session.commit()
            return redirect(url_for('todo.index'))
        flash(error)
    
    return render_template('todo/update.html', todo=todo)

@bp.route('/delete/<uuid:id>')
@login_required
def delete(id):
    todo = get_todo(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todo.index'))