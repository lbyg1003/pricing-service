from flask import Blueprint, render_template, request, redirect, url_for, session
from models.user import User, UserErrors


user_blueprint = Blueprint("users", __name__)


@user_blueprint.route("/register", methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            User.register_user(email, password)

            # when user visiting this endpoint, send user a cookie,
            # allowing flask to identify what session it's related to.

            # when user coming back with the same browser, the browser will send the cookie to the app
            # and flask will populate the session with the user data
            session["email"] = email
            return email
        except UserErrors.UserError as e:
            return e.message

    return render_template("users/register.html")


@user_blueprint.route("/login", methods=["GET", "POST"])
def login_user():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            if User.is_login_valid(email, password):
                session["email"] = email
                return email
        except UserErrors.UserError as e:
            return e.message

    return render_template("users/login.html")