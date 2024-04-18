#!/usr/bin/env python3
"""Basic Auth"""
import base64
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

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        """
        Method that returns the decoded value of a Base64 string
        base64_authorization_header
        Args:
                base64_authorization_header: The Base64 encoded authorization
                header string.

            Returns:
                The decoded value as a UTF-8 string,
                or None if the header is invalid.
        """
        if (base64_authorization_header
           and type(base64_authorization_header) is str):
            try:
                decoded_bytes = base64.b64decode(
                    base64_authorization_header.encode("UTF-8")
                )
                return decoded_bytes
            except (TypeError, base64.binascii.Error):
                return None
        return None
