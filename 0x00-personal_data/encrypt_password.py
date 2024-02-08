#!/usr/bin/env python3
"""Hashing password"""
import bcrypt


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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if a given password matches a previously hashed password

    Args:
        hashed_password (bytes): hashed password to be checked
        password (str): password

    Returns:
        bool: True or False
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
