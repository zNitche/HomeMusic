from flask import Blueprint, redirect, url_for, request
from flask import current_app as app
import flask_login
import os
from datetime import date, datetime
from utils import process_controller
from utils.process import Process


FILES_LOCATION = app.config["FILES_LOCATION"]
LOG_FILES_LOCATION = app.config["LOG_FILES_LOCATION"]

processes_ = Blueprint("processes", __name__, template_folder='template', static_folder='static')


@processes_.route("/processes/cancel_process/<timestamp>", methods=["GET", "POST"])
@flask_login.login_required
def cancel_process(timestamp):
    user_name = flask_login.current_user.id

    log_path = os.path.join(LOG_FILES_LOCATION, user_name, f"{timestamp}.json")

    process_controller.stop_process(log_path, os.path.join(FILES_LOCATION, user_name))

    return redirect(url_for("content.process_details", log_name=timestamp))


@processes_.route("/processes/get_music", methods=["POST"])
@flask_login.login_required
def get_music():
    user_name = flask_login.current_user.id

    music = request.form["content"]

    if music != "":
        music_list = list(music.split("|"))
        timestamp = datetime.now()

        today = date.today()
        hour = timestamp.strftime("%H:%M:%S")
        today = today.strftime("%d:%m:%Y")

        dir_path = os.path.join(FILES_LOCATION, user_name, f"{today}_{hour}")

        timestamp = str(timestamp).replace(" ", "_")
        timestamp = str(timestamp).replace(".", "_")

        log_path = os.path.join(LOG_FILES_LOCATION, user_name)
        log_path = os.path.join(log_path, f"{timestamp}.json")

        download_process = Process(music_list, timestamp, log_path, dir_path)
        download_process.start_process()

        return redirect(url_for("content.process_details", log_name=timestamp))

    else:
        return redirect(url_for("content.home"))
