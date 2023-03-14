from flask import Blueprint, redirect, url_for, request, flash
from flask import current_app as app
import flask_login
import os
import signal
import shutil
from datetime import datetime
from home_music.music_downloader_process import MusicDownloaderProcess
from config import Config
from home_music import models
from home_music import db


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

    try:
        os.kill(pid, signal.SIGTERM)

        app.redis_manager.delete_key(timestamp)

        if os.path.exists(os.path.join(out_path, dir_path)):
            shutil.rmtree(os.path.join(out_path, dir_path))

        log = models.ProcessLog(timestamp=log_data["timestamp"], dir_path=log_data["dir_path"],
                                music_links="".join(log_data["music_links"]),
                                music_names="".join(log_data["music_names"]),
                                was_canceled=log_data["was_canceled"], owner_id=log_data["owner_id"])

        db.session.add(log)
        db.session.commit()

    except Exception as e:
        pass

    return redirect(url_for("content.process_details", timestamp=timestamp))


@processes.route("/processes/get_music", methods=["POST"])
@flask_login.login_required
def get_music():
    user_name = flask_login.current_user.username
    user_id = flask_login.current_user.id

    music_url = request.form["content"]

    if music_url != "":
        music_list = list(music_url.split("|"))

        timestamp = datetime.now()
        timestamp = str(timestamp).replace(" ", "_").replace(".", "_")

        dir_path_root = os.path.join(FILES_LOCATION, user_name)
        dir_path = os.path.join(dir_path_root, timestamp)

        download_process = MusicDownloaderProcess(user_id, app, music_list, timestamp, dir_path, dir_path_root)
        download_process.start_process()

        flash(f"Started process with timestamp {timestamp}", "success")

        return redirect(url_for("content.process_details", timestamp=timestamp))

    else:
        flash("Music URL can't be empty", "error")

        return redirect(url_for("content.home"))
