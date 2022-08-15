from flask import render_template, Blueprint, redirect, url_for, abort
from flask import current_app as app
import flask_login
from home_music.utils import processes_utils


FILES_LOCATION = app.config["FILES_LOCATION"]


content = Blueprint("content", __name__, template_folder='template', static_folder='static')


@content.route("/")
def home():
    if flask_login.current_user.is_authenticated:
        return render_template("index.html")

    else:
        return redirect(url_for("auth.login"))


@content.route("/processes")
@flask_login.login_required
def processes():
    logs_timestamps = app.redis_manager.get_keys()
    logs_data = [app.redis_manager.get_value(timestamp) for timestamp in logs_timestamps]

    running_processes = processes_utils.get_running_processes(logs_data)
    running_processes = list(reversed(sorted(running_processes)))
    finished_processes = list(reversed(sorted([])))

    return render_template("processes.html", log_files=finished_processes, running_log_files=running_processes)


@content.route("/process_details/<timestamp>")
@flask_login.login_required
def process_details(timestamp):
    log_data = app.redis_manager.get_value(timestamp)

    if log_data:
        return render_template("process_details.html", log_data=log_data)

    else:
        abort(404)
