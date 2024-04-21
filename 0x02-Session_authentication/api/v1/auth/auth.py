#!/usr/bin/env python3
"""Template for all authentication system."""
from typing import List, TypeVar
from flask import request
import os


class Auth:
    """Template for all authentication system."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Method to check if authentication is required."""
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        path_with_slash = path if path.endswith("/") else path + "/"

        if path_with_slash in excluded_paths:
            return False

        for excluded_path in excluded_paths:
            if (
                excluded_path.endswith("*")
                and path.startswith(excluded_path[:-1])
            ):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Method to get the authorization header."""
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """Method to get the current user."""
        return None

    def session_cookie(self, request=None):
        """Method that returns a cookie value from a request"""
        if not request:
            return None

        session_name = os.getenv("SESSION_NAME", "_my_session_id")
        return request.cookies.get(session_name)
