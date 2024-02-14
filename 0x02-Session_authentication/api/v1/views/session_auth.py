#!/usr/bin/env python3
""" Module of Session authentication views"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """POST /api/v1/auth_session/login
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not len(email):
        return jsonify({"error": "email missing"}), 400

    if not password or not len(password):
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if not user or not len(user):
        return jsonify({"error": "no user found for this email"}), 404

    for i in user:
        if not i.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

        from api.v1.app import auth
        session_id = auth.create_session(i.id)
        response = jsonify(i.to_json())
        session_name = getenv('SESSION_NAME')
        response.set_cookie(session_name, session_id)
    return response
