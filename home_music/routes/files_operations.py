from flask import Blueprint, send_file, url_for, redirect
from flask import current_app as app
import flask_login
import os


FILES_LOCATION = app.config["FILES_LOCATION"]
LOG_FILES_LOCATION = app.config["LOG_FILES_LOCATION"]


files_operations = Blueprint("files_operations", __name__, template_folder='template', static_folder='static')


@files_operations.route("/files_operations/download/<dir>", methods=["GET", "POST"])
@flask_login.login_required
def download(dir):
    user_name = flask_login.current_user.username

    file_name = f"{dir}.zip"
    file_path = os.path.join(FILES_LOCATION, user_name, file_name)

    return send_file(file_path, as_attachment=False, download_name=file_name, max_age=0)


@files_operations.route("/files_operations/delete/<timestamp>&<dir>", methods=["POST"])
@flask_login.login_required
def delete(timestamp, dir):
    user_name = flask_login.current_user.username

    path_to_zip_file = os.path.join(FILES_LOCATION, user_name, f"{dir}.zip")
    path_to_report_file = os.path.join(LOG_FILES_LOCATION, user_name, f"{timestamp}.json")

    if os.path.exists(path_to_zip_file):
        os.remove(path_to_zip_file)

    os.remove(path_to_report_file)

    return redirect(url_for("content.processes"))
