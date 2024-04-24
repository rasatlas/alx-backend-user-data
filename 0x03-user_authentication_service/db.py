#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Method that save the user to the database.
        Args:
            email(str): email of the user
            password(str): password of the user
        Return:
            User object
        """
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Method that takes in arbitrary keyword arguments and returns
        the first row found in the users table as filtered by the
        method’s input arguments.
        """
        keys = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']
        for key in kwargs.keys():
            if key not in keys:
                raise InvalidRequestError
        result = self._session.query(User).filter_by(**kwargs).first()
        if result is None:
            raise NoResultFound
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates user's attributes as passed in the method's arguments
        then commits changes to the database.
        Args:
            - user_id (int): The ID of the user to be updated.
            - **kwargs: Arbitrary keyword argyments representing user
            attributes to be updated.
        Return:
            None
        Raises:
            - ValueError: If an argument that does not correspond to the user
            attributes is passed.
        """
        keys = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']
        user = self.find_user_by(id=user_id)
        if not user:
            return None
        for key, value in kwargs.items():
            if key in keys:
                setattr(user, key, value)
            else:
                raise ValueError
        self._session.commit()
