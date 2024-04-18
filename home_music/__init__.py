from flask import Flask
import flask_login
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate(compare_type=True)


def register_blueprints(app):
    from home_music.routes import content, auth, errors, files_operations, processes

    app.register_blueprint(content.content)
    app.register_blueprint(auth.auth)
    app.register_blueprint(errors.errors)
    app.register_blueprint(files_operations.files_operations)
    app.register_blueprint(processes.processes)


def setup_app_modules(app):
    from home_music.app_modules.redis_manager import RedisManager

    managers = [RedisManager(0)]

    for manager in managers:
        setattr(app, manager.get_name(), manager)


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    app.secret_key = os.urandom(25)

    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)

    db.init_app(app)

    from home_music import models

    @login_manager.user_loader
    def user_loader(user_id):
        return models.User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

        setup_app_modules(app)
        register_blueprints(app)

        return app
