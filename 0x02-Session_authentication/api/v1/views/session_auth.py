#!/usr/bin/env python3
""" Module of session_auth views
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def auth_session_login():
    """ User login after authentication
    """
    user = None
    email = request.form.get("email")
    pwd = request.form.get("password")
    if not email or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    if not pwd or len(pwd) == 0:
        return jsonify({"error": "password missing"}), 400

    users_list = User.search({'email': email})
    if not users_list:
        return jsonify({"error": "no user found for this email"}), 404
    for users in users_list:
        if users.is_valid_password(pwd):
            user = users
    if not user:
        return jsonify({"error": "wrong password"}), 401

    else:
        from api.v1.app import auth
        user_id = user.id
        session_id = auth.create_session(user_id)
        session_name = getenv('SESSION_NAME')
        user_json = jsonify(user.to_json())
        user_json.set_cookie(session_name, session_id)
        return user_json
