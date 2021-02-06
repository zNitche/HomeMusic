import os


class Config:
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
    FILES_LOCATION = f"{CURRENT_DIR}/files/"
    APP_PORT = 8080
