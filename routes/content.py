from __future__ import unicode_literals
from flask import render_template, Blueprint, redirect, url_for, request, send_file
from flask import current_app as app
import flask_login
import os
import json
from datetime import date, datetime
import process_controller


FILES_LOCATION = app.config["FILES_LOCATION"]
LOG_FILES_LOCATION = app.config["LOG_FILES_LOCATION"]

content_ = Blueprint("content", __name__, template_folder='template', static_folder='static')


@content_.route("/")
def home():
    if flask_login.current_user.is_authenticated:
        return render_template("index.html")
    else:
        return redirect(url_for("auth.login"))


@content_.route("/processes")
@flask_login.login_required
def processes():
    user_name = flask_login.current_user.id

    running_processes, finished_processes = process_controller.get_processes(os.path.join(LOG_FILES_LOCATION, user_name))
    running_processes = list(reversed(sorted(running_processes)))
    finished_processes = list(reversed(sorted(finished_processes)))

    return render_template("processes.html", log_files=finished_processes, running_log_files=running_processes)


@content_.route("/process_details/<log_name>")
@flask_login.login_required
def process_details(log_name):
    user_name = flask_login.current_user.id

    with open(os.path.join(f"{LOG_FILES_LOCATION}{user_name}", f"{log_name}.json")) as file:
        log_data = json.loads(file.read())

    return render_template("process_details.html", log_data=log_data)


@content_.route("/cancel_process/<timestamp>", methods=["GET", "POST"])
@flask_login.login_required
def cancel_process(timestamp):
    user_name = flask_login.current_user.id

    log_path = os.path.join(LOG_FILES_LOCATION, f"{user_name}/{timestamp}.json")

    process_controller.stop_process(log_path, os.path.join(FILES_LOCATION, user_name))

    return redirect(url_for("content.process_details", log_name=f"{timestamp}"))


@content_.route("/main/get_music", methods=["POST"])
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

        dir_name = f"{today}_{hour}"
        dir_path = f"{FILES_LOCATION}{user_name}/{dir_name}"

        timestamp = str(timestamp).replace(" ", "_")
        timestamp = str(timestamp).replace(".", "_")

        log_path = os.path.join(LOG_FILES_LOCATION, user_name)
        log_path = os.path.join(log_path, f"{timestamp}.json")

        download_process = process_controller.Process(music_list, timestamp, log_path, dir_path)
        download_process.start_process()

        return redirect(url_for("content.process_details", log_name=f"{timestamp}"))
    else:
        return redirect(url_for("content.home"))


@content_.route("/main/download/<dir>", methods=["GET", "POST"])
@flask_login.login_required
def download(dir):
    user_name = flask_login.current_user.id

    return send_file(f"{FILES_LOCATION}{user_name}/{dir}.zip",
                     as_attachment=False, attachment_filename=f'{dir}.zip', cache_timeout=0)


@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", message=error)


@app.errorhandler(500)
def overloaded(error):
    return render_template("error.html", message=error)


@app.errorhandler(401)
def non_authenticated(error):
    return redirect(url_for("auth.login"))


@app.errorhandler(405)
def method_not_allowed(error):
    return render_template("error.html", message=error)