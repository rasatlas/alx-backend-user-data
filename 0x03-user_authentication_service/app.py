#!/usr/bin/env python3
"""A basic Flask app"""
from flask import Flask, abort, jsonify, make_response, redirect, request
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
    data = request.form
    email = data.get('email')
    password = data.get('password')
    if AUTH.valid_login(email, password):
        try:
            session_id = AUTH.create_session(email=email)
            response = make_response(jsonify({"email": email,
                                              "message": "logged in"}))
            response.set_cookie('session_id', session_id)
            return response
        except Exception:
            abort(401)
    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """Function to respond to the DELETE /sessions route."""
    session_id = request.cookies.get('session_id')
    try:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect('/')
        else:
            abort(403)
    except Exception:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """Respond to the GET /profile route.
    - The request is expected to contain a session_id cookie.
    Use it to find the user.
    - If the user exists, respond with a 200 HTTP status and
    the following JSON payload: {"email": "<user email>"}
    - If the session ID is invalid or the user does not exist,
    respond with a 403 HTTP status.
    """
    session_id = request.cookies.get('session_id')
    try:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email}), 200
        else:
            abort(403)
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """Respond to the POST /reset_password route
    - The request is expected to contain form data with the 'email' field.
    - If the email is not registered, respond with a 403 status code.
    Otherwise, generate a token and respond with a 200 HTTP status and
    the following JSON payload:
        {"email": "<user email>", "reset_token": "<reset token>"}
    """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
