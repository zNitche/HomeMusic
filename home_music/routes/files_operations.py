from flask import Blueprint, send_file, url_for, redirect
from flask import current_app as app
import flask_login
import os
import shutil
from home_music import db
from home_music import models


FILES_LOCATION = app.config["FILES_LOCATION"]


files_operations = Blueprint("files_operations", __name__, template_folder='template', static_folder='static')


@files_operations.route("/files_operations/<timestamp>/download", methods=["POST"])
@flask_login.login_required
def download(timestamp):
    file_name = f"{timestamp}.zip"
    file_path = os.path.join(FILES_LOCATION, flask_login.current_user.username, file_name)

    return send_file(file_path, as_attachment=False, download_name=file_name, max_age=0)


@files_operations.route("/files_operations/<timestamp>/delete/", methods=["POST"])
@flask_login.login_required
def delete(timestamp):
    user_name = flask_login.current_user.username
    user_id = flask_login.current_user.id

    path_to_zip_file = os.path.join(FILES_LOCATION, user_name, f"{timestamp}.zip")
    path_to_download_dir = os.path.join(FILES_LOCATION, user_name, timestamp)

    if os.path.exists(path_to_zip_file):
        os.remove(path_to_zip_file)

    if os.path.exists(path_to_download_dir):
        shutil.rmtree(path_to_download_dir)

    log = models.ProcessLog.query.filter_by(owner_id=user_id, timestamp=timestamp).first()

    if log:
        db.session.delete(log)
        db.session.commit()

    return redirect(url_for("content.processes"))
