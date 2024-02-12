#!/usr/bin/env python3
"""class to manage the API authentication"""
from api.v1.auth.auth import Auth


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
