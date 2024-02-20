#!/usr/bin/env python3
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash a password with bcrypt.
    Args:
        password (str): The password to be hashed.
    Returns:
        bytes: The salted hash of the password.
    """
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_password
