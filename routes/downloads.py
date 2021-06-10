from flask import Blueprint, send_file
from flask import current_app as app
import flask_login


FILES_LOCATION = app.config["FILES_LOCATION"]

downloads_ = Blueprint("downloads", __name__, template_folder='template', static_folder='static')


@downloads_.route("/downloads/download/<dir>", methods=["GET", "POST"])
@flask_login.login_required
def download(dir):
    user_name = flask_login.current_user.id

    return send_file(f"{FILES_LOCATION}{user_name}/{dir}.zip",
                     as_attachment=False, attachment_filename=f'{dir}.zip', cache_timeout=0)
