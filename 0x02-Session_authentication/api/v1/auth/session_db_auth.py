#!/usr/bin/env python3
"""User session model"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """Authentication class"""
    def create_session(self, user_id=None):
        """Overload the create session method"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        arg = {"user_id": user_id, "session_id": session_id}
        user_session = UserSession(**arg)
        user_session.save()
        user_session.save_to_file()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Overload user id for session id"""
        if session_id is None:
            return None

        UserSession.load_from_file()
        user_session = UserSession.search({
            'session_id': session_id
        })

        if not user_session:
            return None

        user_session = user_session[0]

        expired_time = user_session.created_at + \
            timedelta(seconds=self.session_duration)

        if expired_time < datetime.utcnow():
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """Overload destroy session"""
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        user_session = UserSession.search({"session_id": session_id})
        if not user_session:
            return False
        user_session[0].remove()
        UserSession.save_to_file()
        return True
