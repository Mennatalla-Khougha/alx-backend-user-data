#!/usr/bin/env python3
"""class SessionExpAuth"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """class SessionExpAuth"""
    def __init__(self):
        """Initialize the class"""
        self.session_duration = int(getenv('SESSION_DURATION', '0'))

    def create_session(self, user_id=None):
        """Overload the create session method"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Overload the user id for session id method"""
        if not session_id:
            return None
        session_dict = super().user_id_by_session_id.get(session_id)
        if not session_dict:
            return None
        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        created_at = session_dict.get('created_at')
        if not created_at:
            return None
        exp = created_at + timedelta(seconds=self.session_duration)
        if exp < datetime.now():
            return None
        return session_dict.get('user_id')
