#!/usr/bin/env python3
""" Module of Session authentication views
"""
import os
from flask import jsonify, request
from api.v1 import auth
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Handle user login with session authentication
        POST /api/v1/auth_session/login
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if email or password is missing
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Retrieve the User instance based on the email
    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    # Check if the password is correct
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create a session ID for the User ID
    session_id = auth.create_session(user.id)

    # Return the user dictionary representation and set the session cookie
    response = jsonify(user.to_json())
    response.set_cookie(
        os.getenv("SESSION_NAME", "_my_session_id"),
        session_id
        )
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def handle_logout():
    """
    Handle user logout
    """
    if auth.destroy_session(request):
        return jsonify({}), 200
    os.abort(404)
