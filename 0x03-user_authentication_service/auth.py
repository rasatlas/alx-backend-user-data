#!/usr/bin/env python3
"""
auth module
"""
from typing import Optional
import uuid
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Method that takes in a password string arguments and
    returns bytes."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """Generate a UUID and return its string representation."""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """If a user with the given password does not exist in the database
        it will save it to the database. If a user exists it will raise a
        ValueError.
        Args:
            - email (str): email of user
            - password (str): password of user
        Return:
            - user : Returns user saved into the database
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists.".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Locate the user by email. If it exists, check the password with
        bcrypt.checkpw. If it matches return True.
        In any other case, return False
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """Finds the user correponding to the email,
        generate a new UUID and store it in the database as the
        user's session_id, then return the session ID.
        """
        session_id = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user_id=user.id, session_id=session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self,
                                 session_id: Optional[str]) -> Optional[User]:
        """Retrieve the corresponding User object for the provided session ID.
        Args:
            - session_id (str): The session ID of the user to be retrieved.
        Returns:
            - User or None: If the session ID is None or no user is found,
            return None. Otherwise, return the corresponding User object.
        """
        if session_id is not None:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except Exception:
                return None
        return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy the corresponding user session for the provided user id
        Args:
            - user_id (int): id of the user
        Returns:
            - None
        """
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Find the user corresponding to the email.
        If the user does not exist, raise a ValueError excepton.
        If it exists, generate a UUID and update the user's reset_token
        databae field.
        Args:
            - email (str): email of the user
        Returns:
            - new_token (str): the generated restet_token
        """
        new_token = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, reset_token=new_token)
            return new_token
        except Exception:
            return ValueError
