from flask import render_template, Blueprint, redirect, url_for
from flask import current_app as app
import flask_login
import os
import json
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
    user_name = flask_login.current_user.username

    running_processes, finished_processes = [], []
    running_processes = list(reversed(sorted(running_processes)))
    finished_processes = list(reversed(sorted(finished_processes)))

    return render_template("processes.html", log_files=finished_processes, running_log_files=running_processes)


@content.route("/process_details/<log_name>")
@flask_login.login_required
def process_details(log_name):
    user_name = flask_login.current_user.username

    return render_template("process_details.html", log_data={})
