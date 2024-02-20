#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

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
        """ The method should save the user to the database

        Args:
            email (str): User's Email
            hashed_password (str): User's hashed password

        Returns:
            User (object): User object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by arbitrary keyword arguments.

        Args:
            **kwargs: Keyword arguments to filter the User table.

        Returns:
            User: The first User object found that matches the filter.

        Raises:
            NoResultFound: If no user is found that matches the filter.
            InvalidRequestError: If the query arguments are invalid.
        """
        # if not kwargs:
        #     raise InvalidRequestError
        # user = self._session.query(User).filter_by(**kwargs).first()
        # if not user:
        #     raise NoResultFound
        # return user

        if not kwargs:
            raise InvalidRequestError
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound
        return user
        # except InvalidRequestError:

    def update_user(self, user_id: int, **kwargs) -> None:
        """locate the user to update, then will update the user’s attributes

        Args:
            user_id (int): User ID to update.
            **kwargs: Keyword arguments to update the user's attributes.

        Raises:
            ValueError: If an argument does not correspond to a user attribute.
        """
        user = self.find_user_by(id=user_id)
        if not user:
            raise ValueError

        for attr, value in kwargs.items():
            if hasattr(user, attr):
                setattr(user, attr, value)
            else:
                raise ValueError

        self.__session.commit()
