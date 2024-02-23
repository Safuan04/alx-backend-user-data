#!/usr/bin/env python3
""" Creating flask app
"""
from flask import Flask, jsonify, request, abort
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

    if AUTH.valid_login(user_email, user_pwd) == False:
        abort(401)

    session_id = AUTH.create_session(user_email)
    response = jsonify({"email": f"{user_email}", "message": "logged in"})
    response.set_cookie('session_id', session_id)

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
