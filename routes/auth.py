from flask import render_template, request, redirect, url_for, Blueprint
import flask_login
from users import user
from users import users_accounts as users
from passlib.hash import sha256_crypt


auth_ = Blueprint("auth", __name__, template_folder='template', static_folder='static')


@auth_.route("/auth/login")
def login():
    is_user_authenticated = flask_login.current_user.is_authenticated

    if is_user_authenticated:
        return redirect(url_for("content.home"))
    else:
        message = ""
        return render_template("login.html", message=message, is_user_authenticated=is_user_authenticated)


@auth_.route("/auth/login/check", methods=["POST"])
def check():
    if flask_login.current_user.is_authenticated:
        return redirect(url_for("content.home"))
    else:
        try:
            users_accounts = users.UsersAccounts.users

            username = request.form["user_name"]

            if sha256_crypt.verify(request.form["password"], users_accounts[username]["password"]):
                user_model = user.User()
                user_model.id = username

                flask_login.login_user(user_model)

                return redirect(url_for("content.home"))
            else:
                message = "Wrong username or password"
                return render_template("login.html", message=message)

        except:
            message = "Wrong username or password"
            return render_template("login.html", message=message)


@auth_.route("/auth/logout", methods=["POST", "GET"])
@flask_login.login_required
def logout():
    flask_login.logout_user()

    return redirect(url_for("content.home"))

