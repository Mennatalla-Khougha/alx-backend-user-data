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
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Updates the corresponding user’s session ID to None

        Args:
            user_id (int): The user ID
        """
        user = self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Generate a UUID and update the user’s reset_token database field

        Args:
            email (str): User email

        Returns:
            str: The reset token
        """
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates a user's password
        Args:
            reset_token (str): reset_token issued to reset the password
            password (str): user's new password
        Return:
            None
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()

        hashed = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed, reset_token=None)
