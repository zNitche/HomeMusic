from flask import Blueprint, send_file, url_for, redirect
from flask import current_app as app
import flask_login
import os
from home_music.utils import processes_utils


FILES_LOCATION = app.config["FILES_LOCATION"]
LOG_FILES_LOCATION = app.config["LOG_FILES_LOCATION"]


files_operations = Blueprint("files_operations", __name__, template_folder='template', static_folder='static')


@files_operations.route("/files_operations/<dir>/download", methods=["POST"])
@flask_login.login_required
def download(dir):
    file_name = f"{dir}.zip"
    file_path = os.path.join(FILES_LOCATION, flask_login.current_user.username, file_name)

    return send_file(file_path, as_attachment=False, download_name=file_name, max_age=0)


@files_operations.route("/files_operations/<timestamp>/delete/", methods=["POST"])
@flask_login.login_required
def delete(timestamp):
    user_name = flask_login.current_user.username

    log_data = processes_utils.get_process_data(os.path.join(LOG_FILES_LOCATION, user_name), f"{timestamp}.json")

    path_to_zip_file = os.path.join(FILES_LOCATION, user_name, f"{log_data['dir_path']}.zip")
    path_to_report_file = os.path.join(LOG_FILES_LOCATION, user_name, f"{timestamp}.json")

    if os.path.exists(path_to_zip_file):
        os.remove(path_to_zip_file)

    os.remove(path_to_report_file)

    return redirect(url_for("content.processes"))
