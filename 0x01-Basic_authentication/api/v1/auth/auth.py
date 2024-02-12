#!/usr/bin/env python3
"""class to manage the API authentication"""
from flask import request
from typing import List, TypeVar


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
            if path.rstrip('/') == i.rstrip('/'):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Public method

        Args:
            request (_type_, optional): _description_. Defaults to None.

        Returns:
            str: None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Public method
        """
        return None
