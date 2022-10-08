import os
from consts import DBConsts


class Config:
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

    APP_DIR = os.path.join(CURRENT_DIR, "home_music")
    FILES_LOCATION = os.path.join(CURRENT_DIR, "files")
    LOG_FILES_LOCATION = os.path.join(CURRENT_DIR, "logs")

    MIGRATIONS_DIR_PATH = os.path.join(CURRENT_DIR, "migrations")

    APP_PORT = 8080
    APP_HOST = "0.0.0.0"
    DEBUG_MODE = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_MYSQL_DATABASE_URI = "mysql://root:{password}@{address}/{db_name}"
    SQLALCHEMY_SQLITE_DATABASE_URI = f"sqlite:////{CURRENT_DIR}/database/app.db"

    SQLALCHEMY_DATABASE_URI = ""

    DB_MODE = os.environ.get("DB_MODE", default=DBConsts.SQLITE_DB)
