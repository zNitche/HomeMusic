from flask import Blueprint, redirect, url_for, request, flash
from flask import current_app as app
import flask_login
import os
import signal
import shutil
from datetime import date, datetime
from home_music.process import Process
from config import Config


FILES_LOCATION = app.config["FILES_LOCATION"]


processes = Blueprint("processes", __name__, template_folder='template', static_folder='static')


@processes.route("/processes/<timestamp>/cancel", methods=["POST"])
@flask_login.login_required
def cancel_process(timestamp):
    out_path = os.path.join(Config.FILES_LOCATION, flask_login.current_user.username)

    log_data = app.redis_manager.get_value(timestamp)

    pid = log_data["process_pid"]
    dir_path = log_data["dir_path"]
    log_data["is_running"] = False
    log_data["was_canceled"] = True
    log_data["process_pid"] = None

    try:
        os.kill(pid, signal.SIGTERM)

    except Exception as e:
        pass

    if os.path.exists(os.path.join(out_path, dir_path)):
        shutil.rmtree(os.path.join(out_path, dir_path))

    return redirect(url_for("content.process_details", log_name=timestamp))


@processes.route("/processes/get_music", methods=["POST"])
@flask_login.login_required
def get_music():
    user_name = flask_login.current_user.username

    music_url = request.form["content"]

    if music_url != "":
        music_list = list(music_url.split("|"))
        timestamp = datetime.now()

        today = date.today()
        hour = timestamp.strftime("%H:%M:%S")
        today = today.strftime("%d:%m:%Y")

        dir_path = os.path.join(FILES_LOCATION, user_name, f"{today}_{hour}")

        timestamp = str(timestamp).replace(" ", "_").replace(".", "_")

        download_process = Process(app, music_list, timestamp, dir_path)
        download_process.start_process()

        flash(f"Started process with timestamp {timestamp}", "success")

        return redirect(url_for("content.process_details", log_name=timestamp))

    else:
        flash("Music URL can't be empty", "error")

        return redirect(url_for("content.home"))
