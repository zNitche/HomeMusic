from flask import render_template, request, redirect, url_for, Blueprint
import flask_login
from users import User
from users import users_accounts as users
from passlib.hash import sha256_crypt


auth_ = Blueprint("auth", __name__, template_folder='template', static_folder='static')


@auth_.route("/login")
def login():
    if flask_login.current_user.is_authenticated:
        return redirect(url_for("content.home"))
    else:
        message = ""
        return render_template("login.html", message=message)


@auth_.route("/login/check", methods=["POST"])
def check():
    if flask_login.current_user.is_authenticated:
        return redirect(url_for("content.home"))
    else:
        try:
            users_accounts = users.UsersAccounts.users

            username = request.form["user_name"]

            if sha256_crypt.verify(request.form["password"], users_accounts[username]["password"]):
                user = User.User()
                user.id = username

                flask_login.login_user(user)

                return redirect(url_for("content.home"))
            else:
                message = "Wrong username or password"
                return render_template("login.html", message=message)

        except:
            message = "Wrong username or password"
            return render_template("login.html", message=message)


@auth_.route("/logout", methods=["POST", "GET"])
@flask_login.login_required
def logout():
    flask_login.logout_user()

    return redirect(url_for("content.home"))

