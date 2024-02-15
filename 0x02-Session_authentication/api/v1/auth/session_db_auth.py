#!/usr/bin/env python3
"""User session model"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Authentication class"""
    def create_session(self, user_id=None):
        """Overload the create session method"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        user_session = UserSession({
            "user_id": user_id, "session_id": session_id})
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Overload user id for session id"""
        user_session = UserSession.search({"session_id": session_id})
        if not user_session:
            return None
        return user_session

    def destroy_session(self, request=None):
        """Overload destroy session"""
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_session = UserSession.search({"session_id": session_id})
        if not user_session:
            return False
        del user_session[0]
        return True
