import flask_migrate
import os
from home_music import create_app
from home_music import db, migrate


def main():
    app = create_app()
    migrations_dir_path = app.config["MIGRATIONS_DIR_PATH"]

    with app.app_context():
        migrate.init_app(app, db, directory=migrations_dir_path)

        if not os.path.exists(migrations_dir_path):
            flask_migrate.init(migrations_dir_path)

        flask_migrate.migrate(migrations_dir_path)
        flask_migrate.upgrade(migrations_dir_path)


if __name__ == '__main__':
    main()