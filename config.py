import os


class Config:
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

    APP_DIR = os.path.join(CURRENT_DIR, "home_music")
    FILES_LOCATION = os.path.join(APP_DIR, "files")
    LOG_FILES_LOCATION = os.path.join(APP_DIR, "logs")

    APP_PORT = 8080
    APP_HOST = "0.0.0.0"
    DEBUG_MODE = False
