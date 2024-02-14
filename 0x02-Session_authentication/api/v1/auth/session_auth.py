#!/usr/bin/env python3
"""class to manage the Session authentication"""
from api.v1.auth.auth import Auth
from uuid import uuid4


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
        self.user_id_by_session_id[user_id] = session_id
        return session_id
