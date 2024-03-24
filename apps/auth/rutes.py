from flask import Blueprint, render_template, request, url_for, redirect, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from .models import UserModel
from core import db



bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        elif UserModel.query.filter_by(username=username).first() is not None:
            error = f'User {username} is already registered'
        
        if error is None:
            user = UserModel(username, generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login', registered=True))
        flash(error)
    if g.user:
        return redirect(url_for('todo.index'))
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = UserModel.query.filter_by(username=username).first()
        if user is None:
            error = 'Incorrect username or password'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect username or password'
        
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('todo.index'))
        flash(error)
    if g.user:
        return redirect(url_for('todo.index'))
    return render_template('auth/login.html', success=request.args.get('registered'))

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        user = UserModel.query.filter_by(id=user_id).first()
        if user is None:
            g.user = None
        else:
            g.user = user
