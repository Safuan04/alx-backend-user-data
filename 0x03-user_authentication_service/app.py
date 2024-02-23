#!/usr/bin/env python3
""" Creating flask app
"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index():
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """Register user if it doest exist"""
    user_email = request.form.get('email')
    user_pwd = request.form.get('password')

    try:
        user = AUTH.register_user(user_email, user_pwd)
        return jsonify({"email": f"{user.email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ Login function
    """
    user_email = request.form.get('email')
    user_pwd = request.form.get('password')

    if AUTH.valid_login(user_email, user_pwd) is False:
        abort(401)

    session_id = AUTH.create_session(user_email)
    response = jsonify({"email": f"{user_email}", "message": "logged in"})
    response.set_cookie('session_id', session_id)

    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ Logout function
    """
    session_id = request.cookies.get('session_id')

    try:
        user = AUTH.get_user_from_session_id(session_id)
        AUTH.destroy_session(user.id)
        redirect(url_for("index"))
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
