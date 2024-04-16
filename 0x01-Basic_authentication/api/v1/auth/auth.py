from typing import List, TypeVar
from flask import request

"""Template for all authentication system."""


class Auth:
    """Template for all authentication system."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require_auth method."""
        return False

    def authorization_header(self, request=None) -> str:
        """authorization_header method."""
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """current_user method."""
        return None
