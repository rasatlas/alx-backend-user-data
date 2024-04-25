#!/usr/bin/env python3
"""A basic Flask app"""
from flask import Flask, abort, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    """Home route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """End-point to register a user.
    - The end-point should expect two form data fields:
        - email
        - password.
    - If the user does not exist, the end-point should register it and
    respond with a JSON payload.
    - If the user is already registered, catch the exception and return
    JSON payload of the form.
    """
    data = request.form
    email = data.get('email')
    password = data.get('password')
    if email and password:
        try:
            AUTH.register_user(email, password)
            return jsonify({"email": email, "message": "user created"})
        except ValueError:
            return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """Creates a new session for the user, stores the session Id as a cookie
    with key 'session_id' on the response and return a JSON paylod to the form.
    """
    cookie = {}
    data = request.form
    email = data.get('email')
    password = data.get('password')
    if AUTH.valid_login(email, password):
        try:
            cookie['session_id'] = AUTH.create_session(email=email)
            return jsonify({"email": email, "message": "logged in"})
        except Exception:
            abort(401)
    abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
