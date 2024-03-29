#!/usr/bin/env python3
"""class to manage the API authentication"""
from api.v1.auth.auth import Auth
from models.user import User
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """Class BasicAuth that inherits from Auth"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extract base64 authorization header

        Args:
            authorization_header (str): The authorization header

        Returns:
            str: _description_
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic"):
            return None
        header = authorization_header.split(' ')
        if len(header) != 2:
            return None
        return header[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decode base64 authorization header

        Args:
            base64_authorization_header (str): coded authorization header

        Returns:
            str: _description_
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decode_base = base64.b64decode(
                base64_authorization_header.encode())
            value = decode_base.decode('utf-8')
        except Exception:
            return None
        return value

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Extract user credentials

        Args:
            decoded_base64_authorization_header (str): Authorization header

        Return:
            (str, str): User email and password from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """User object from credentials

        Args:
            user_email (str): User Email
            user_pwd (str): User password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
            if not users or not len(users):
                return None
            if not users[0].is_valid_password(user_pwd):
                return None
            return users[0]
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        if request is None:
            return None
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        base64_auth_header = self.extract_base64_authorization_header(
            auth_header)
        if base64_auth_header is None:
            return None
        decoded_auth_header = self.decode_base64_authorization_header(
            base64_auth_header)
        if decoded_auth_header is None:
            return None
        user_email, user_pwd = self.extract_user_credentials(
            decoded_auth_header)
        if user_email is None or user_pwd is None:
            return None
        return self.user_object_from_credentials(user_email, user_pwd)
