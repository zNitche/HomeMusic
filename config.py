import os


class Config:
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

    APP_DIR = os.path.join(CURRENT_DIR, "home_music")
    FILES_LOCATION = os.path.join(CURRENT_DIR, "files")
    LOG_FILES_LOCATION = os.path.join(CURRENT_DIR, "logs")

    MIGRATIONS_DIR_PATH = os.path.join(CURRENT_DIR, "migrations")
    SQLALCHEMY_DATABASE_URI = f"sqlite:////{CURRENT_DIR}/database/app.db"
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 10,
        "pool_pre_ping": True
    }

    APP_PORT = 8080
    APP_HOST = "0.0.0.0"
    DEBUG_MODE = False
