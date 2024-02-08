#!/usr/bin/env python3
import bcrypt
"""Hashing password"""


def hash_password(password: str) -> bytes:
    """hash_password function that expects one string argument name password
    and returns a salted, hashed password, which is a byte string

    Args:
        password (str): password to be hashed

    Returns:
        bytes: hashed password
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
