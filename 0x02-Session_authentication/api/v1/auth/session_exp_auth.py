#!/usr/bin/env python3
"""class SessionExpAuth"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """class SessionExpAuth"""
    def __init__(self):
        """Initialize the class"""
        super().__init__()
        self.session_duration = int(getenv('SESSION_DURATION', '0'))
        self.user_id_by_session_id = {}

    def create_session(self, user_id=None):
        """Overload the create session method"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Overload the user id for session id method"""
        if not session_id:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None
        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict['user_id']
        created_at = session_dict['created_at']
        if not created_at:
            return None
        exp = created_at + timedelta(seconds=self.session_duration)
        if exp < datetime.now():
            return None
        return session_dict['user_id']
