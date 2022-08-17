from flask import render_template, Blueprint, redirect, url_for, abort
from flask import current_app as app
import flask_login
from home_music.utils import processes_utils
from home_music import models


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

    finished_processes = models.ProcessLog.query.filter_by(owner_id=flask_login.current_user.id).all()
    finished_processes = [log.timestamp for log in finished_processes]

    running_processes_data = processes_utils.get_running_processes_data(logs_data, flask_login.current_user.id)
    running_processes_timestamps = [log_data["timestamp"] for log_data in running_processes_data]

    running_processes = list(reversed(sorted(running_processes_timestamps)))
    finished_processes = list(reversed(sorted(finished_processes)))

    return render_template("processes.html", log_files=finished_processes, running_log_files=running_processes)


@content.route("/process_details/<timestamp>")
@flask_login.login_required
def process_details(timestamp):
    archive_log_data = models.ProcessLog.query.filter_by(owner_id=flask_login.current_user.id, timestamp=timestamp).first()

    running_log_data = app.redis_manager.get_value(timestamp)

    log_data = archive_log_data.__dict__ if archive_log_data else running_log_data

    if log_data:
        if log_data["owner_id"] == flask_login.current_user.id:
            return render_template("process_details.html", log_data=log_data)

    abort(404)
