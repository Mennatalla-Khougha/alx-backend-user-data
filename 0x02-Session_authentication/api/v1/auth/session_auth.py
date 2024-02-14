#!/usr/bin/env python3
"""class to manage the Session authentication"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """class to manage the Session authentication"""
    user_id_by_session_id: dict = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a user_id

        Args:
            user_id (str): The User ID. Defaults to None.

        Returns:
            str: The session ID
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ returns a User ID based on a Session ID

        Args:
            session_id (str): The Session ID. Defaults to None.

        Returns:
            str: The User Id
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return str(self.user_id_by_session_id.get(session_id))

    def current_user(self, request=None):
        """Returns a User instance based on a cookie value

        Args:
            request : Defaults to None.
        """
        cookie = self.session_cookie(request)
        id = self.user_id_for_session_id(cookie)
        return User.get(id)

    def destroy_session(self, request=None):
        """Deletes the user session / logout"""
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id or not self.user_id_for_session_id(session_id):
            return False
        del self.user_id_by_session_id[session_id]
        return True
