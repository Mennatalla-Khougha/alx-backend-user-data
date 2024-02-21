#!/usr/bin/env python3
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """Hash a password with bcrypt.
    Args:
        password (str): The password to be hashed.
    Returns:
        bytes: The salted hash of the password.
    """
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_password


def _generate_uuid() -> str:
    """Generate a new UUID and return it as a string.

    Returns:
        str: A new UUID as a string.
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user

        Args:
            email (str): User email
            password (str): User password

        Returns:
            User: User Object

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists.")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """Locate the user by email. If it exists, check the password.

        Args:
            email (str): User's email
            password (str): User password

        Returns:
            bool: True -> valid user, False -> non valid user
        """
        try:
            user = self._db.find_user_by(email=email)
            if not user:
                return False
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Create a new session for the user with the given email.

        Args:
            email (str): User's email

        Returns:
            str: The session ID as a string.
        """
        try:
            user = self._db.find_user_by(email=email)
            if not user:
                return None
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """Get the user using session id

        Args:
            session_id (str): The session ID

        Returns:
            User: The User
        """
        if not session_id:
            return None
        user = self._db.find_user_by(session_id=session_id)
        if not user:
            return None
        return user
