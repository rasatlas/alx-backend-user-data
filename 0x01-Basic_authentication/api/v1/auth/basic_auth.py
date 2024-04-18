#!/usr/bin/env python3
"""Basic Auth"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Basic Authentication class that inherits from Auth."""

    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        """Extracts the Base64 part of the Authorization header
        for a Basic Authentication.
        """
        if (
            authorization_header
            and type(authorization_header) is str
            and authorization_header.startswith("Basic ")
        ):
            base64_str = authorization_header.split()
            return base64_str[1]
        return None
