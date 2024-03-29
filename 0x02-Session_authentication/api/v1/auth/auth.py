#!/usr/bin/env python3
"""class to manage the API authentication"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """class to manage the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if the specified path require authentication

        Args:
            path (str): Path to be checked
            excluded_paths (List[str]): paths excluded from authentication

        Returns:
            bool: True, False
        """
        if path is None:
            return True
        if not excluded_paths or excluded_paths is None:
            return True
        for i in excluded_paths:
            if i[-1] == "*":
                if path.startswith(i[:-1]):
                    return False
            if path.rstrip('/') == i.rstrip('/'):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Extract the Authorization header from the request.

        Args:
            request: The request object.

        Returns:
            str: The Authorization header value if present, otherwise None.
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Public method"""
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request

        Args:
            request : Defaults to None.
        """
        if request is None:
            return None
        session_name = getenv('SESSION_NAME')
        cookie_value = request.cookies.get(session_name)
        return cookie_value
