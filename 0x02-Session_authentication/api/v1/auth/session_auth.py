#!/usr/bin/env python3
"""Session_auth"""
from uuid import uuid4
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """class SessionAuth"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Method that creates a Session ID for a user_id"""
        if user_id is None or type(user_id) is not str:
            return None
        # Covnert uuid to string
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Method that returns a User ID based on a session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Overloaded method that returns a User instance
        based on a cookie value"""
        # Get the session ID from the session cookie
        session_id = self.session_cookie(request)

        if session_id:
            # Get the user ID corresponding to the session ID
            user_id = self.user_id_for_session_id(session_id)

            if user_id:
                # Retrieve the user instance from the database
                user = User.get(user_id)
                return user

        return None

    def destroy_session(self, request=None):
        """Method that deletes the user session/logout"""
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True
