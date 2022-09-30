import os
import multiprocessing


class Config:
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

    APP_DIR = os.path.join(CURRENT_DIR, "home_music")
    FILES_LOCATION = os.path.join(CURRENT_DIR, "files")
    LOG_FILES_LOCATION = os.path.join(CURRENT_DIR, "logs")

    MIGRATIONS_DIR_PATH = os.path.join(CURRENT_DIR, "migrations")

    APP_PORT = 8080
    APP_HOST = "0.0.0.0"
    DEBUG_MODE = False

    SQLALCHEMY_DATABASE_URI = "mysql://root:{password}@{address}/{db_name}"

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": multiprocessing.cpu_count() - 1 + 10,
        "pool_recycle": 10,
        "pool_pre_ping": True
    }
