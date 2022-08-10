from flask import Flask
import flask_login
from home_music.users import user
from home_music.users import users_accounts
from flask_sqlalchemy import SQLAlchemy
import os
from config import Config


db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    app.secret_key = os.urandom(25)

    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)

    users = users_accounts.UsersAccounts.users

    app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI.format(
        password=os.environ.get("MYSQL_ROOT_PASSWORD"),
        address=os.environ.get("MYSQL_SERVER_HOST"),
        db_name=os.environ.get("DB_NAME")
    )

    db.init_app(app)

    from home_music import models

    @login_manager.user_loader
    def user_loader(username):

        if username not in users:
            return

        user_model = user.User()
        user_model.id = username
        return user_model

    with app.app_context():
        db.create_all()

        from home_music.routes import content, auth, errors, files_operations, processes

        app.register_blueprint(content.content)
        app.register_blueprint(auth.auth)
        app.register_blueprint(errors.errors)
        app.register_blueprint(files_operations.files_operations)
        app.register_blueprint(processes.processes)

        return app
