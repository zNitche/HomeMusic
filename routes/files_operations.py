from flask import Blueprint, send_file, url_for, redirect
from flask import current_app as app
import flask_login
import os


FILES_LOCATION = app.config["FILES_LOCATION"]
LOG_FILES_LOCATION = app.config["LOG_FILES_LOCATION"]

files_operations_ = Blueprint("files_operations", __name__, template_folder='template', static_folder='static')


@files_operations_.route("/files_operations/download/<dir>", methods=["GET", "POST"])
@flask_login.login_required
def download(dir):
    user_name = flask_login.current_user.id

    return send_file(f"{FILES_LOCATION}{user_name}/{dir}.zip",
                     as_attachment=False, attachment_filename=f'{dir}.zip', cache_timeout=0)


@files_operations_.route("/files_operations/delete/<timestamp>&<dir>", methods=["POST"])
@flask_login.login_required
def delete(timestamp, dir):
    user_name = flask_login.current_user.id

    path_to_zip_file = f"{FILES_LOCATION}{user_name}/{dir}.zip"
    path_to_report_file = f"{LOG_FILES_LOCATION}{user_name}/{timestamp}.json"

    if os.path.exists(path_to_zip_file):
        os.remove(path_to_zip_file)

    os.remove(path_to_report_file)

    return redirect(url_for("content.processes"))
