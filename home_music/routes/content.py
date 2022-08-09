from flask import render_template, Blueprint, redirect, url_for
from flask import current_app as app
import flask_login
import os
import json
from home_music.utils import processes_utils


FILES_LOCATION = app.config["FILES_LOCATION"]
LOG_FILES_LOCATION = app.config["LOG_FILES_LOCATION"]


content = Blueprint("content", __name__, template_folder='template', static_folder='static')


@content.route("/")
def home():
    is_user_authenticated = flask_login.current_user.is_authenticated

    if is_user_authenticated:
        return render_template("index.html", is_user_authenticated=is_user_authenticated)
    else:
        return redirect(url_for("auth.login"))


@content.route("/processes")
@flask_login.login_required
def processes():
    user_name = flask_login.current_user.id
    is_user_authenticated = flask_login.current_user.is_authenticated

    running_processes, finished_processes = processes_utils.get_processes(os.path.join(LOG_FILES_LOCATION, user_name))
    running_processes = list(reversed(sorted(running_processes)))
    finished_processes = list(reversed(sorted(finished_processes)))

    return render_template("processes.html", log_files=finished_processes, running_log_files=running_processes,
                           is_user_authenticated=is_user_authenticated)


@content.route("/process_details/<log_name>")
@flask_login.login_required
def process_details(log_name):
    user_name = flask_login.current_user.id
    is_user_authenticated = flask_login.current_user.is_authenticated

    with open(os.path.join(LOG_FILES_LOCATION, user_name, f"{log_name}.json")) as file:
        log_data = json.loads(file.read())

    return render_template("process_details.html", log_data=log_data,
                           is_user_authenticated=is_user_authenticated)
