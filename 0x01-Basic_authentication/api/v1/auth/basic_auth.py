#!/usr/bin/env python3
"""Basic Auth"""
import base64
from typing import Tuple, TypeVar
from api.v1.auth.auth import Auth
from models.user import User


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
                    base64_authorization_header, validate=True
                )
                return decoded_bytes.decode('UTF-8')
            except (TypeError, base64.binascii.Error):
                return None
        return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> Tuple[str, str]:
        """
        Method that returns the user email and password from the
        Base64 decoded value.
        Args:
            decoded_base64_authorization_header: The base64 decoded value
        Returns:
            A tuple containing email and password
        """
        if (
            decoded_base64_authorization_header
            and type(decoded_base64_authorization_header) is str
            and ":" in decoded_base64_authorization_header
        ):
            return (decoded_base64_authorization_header.split(":"))
        return None, None

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
            ) -> TypeVar('User'):
        """
        Method that returns the 'User' instance based on his email and password
        Args:
            user_email: email of the user
            user_pwd: password of the user
        Returns:
            User object which instance of User class.
        """
        if type(user_email) is str and type(user_pwd) is str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Method that overloads 'Auth' and retrieves the 'User' instance
        for a request
        Args:
            request:
        Returns:
            User:
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)
