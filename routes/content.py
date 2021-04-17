from __future__ import unicode_literals
from flask import render_template, Blueprint, redirect, url_for, request, send_file
from flask import current_app as app
import flask_login
import os
import youtube_dl
from datetime import date, datetime


FILES_LOCATION = app.config["FILES_LOCATION"]

content_ = Blueprint("content", __name__, template_folder='template', static_folder='static')


@content_.route("/")
def home():
    if flask_login.current_user.is_authenticated:
        return render_template("index.html")
    else:
        return redirect(url_for("auth.login"))


@content_.route("/main/get_music", methods=["POST"])
@flask_login.login_required
def get_music():
    user_name = flask_login.current_user.id

    for dir in os.listdir(f"{FILES_LOCATION}{user_name}"):
        os.system(f"rm -rf {FILES_LOCATION}{user_name}/{dir}")

    music = request.form["content"]

    if music != "":
        music_list = music.split("|")

        today = date.today()
        hour = datetime.now()
        hour = hour.strftime("%H:%M:%S")
        today = today.strftime("%d:%m:%Y")

        dir_name = f"{today}_{hour}"
        dir_path = f"{FILES_LOCATION}{user_name}/{dir_name}"

        if os.path.exists(dir_path):
            os.remove(dir_path)

        os.mkdir(dir_path)

        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "outtmpl": f"{dir_path}/%(title)s.%(ext)s",
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(music_list)

        return redirect(url_for("content.download", dir=dir_name))
    else:
        return redirect(url_for("content.home"))


@content_.route("/main/download/<dir>", methods=["GET"])
@flask_login.login_required
def download(dir):
    user_name = flask_login.current_user.id

    os.system(f"zip -r -j {FILES_LOCATION}{user_name}/{dir}.zip {FILES_LOCATION}{user_name}/{dir}")
    os.system(f"rm -rf {FILES_LOCATION}{user_name}/{dir}")

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