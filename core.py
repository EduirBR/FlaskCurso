from decouple import config
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        DEBUG = config('DEBUG', default=True, cast=bool),
        SECRET_KEY=config('SECRET_KEY', default='insecurekeyfordev'),
        SQLALCHEMY_DATABASE_URI=config('DATABASE_URL', default='sqlite:///db.sqlite3'),
    )
    db.init_app(app)
    #Registrar BluePrints
    from apps.todos import rutes as todos
    app.register_blueprint(todos.bp)
    
    from apps.auth import rutes as auth
    app.register_blueprint(auth.bp)
    
    @app.route('/')
    @app.route('/index')
    def index():
        return render_template('index.html')

    with app.app_context():
        db.create_all()
    return app
