#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """Registers a new user with the specified email and password."""
    res = requests.post(BASE_URL + "/users",
                        data={'email': email, "password": password})
    if res.status_code == 200:
        assert(res.json() == {"email": email, "message": "user created"})
    else:
        assert(res.status_code == 400)
        assert(res.json() == {"message": "email already registered"})


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempts to log in with the specified email and incorrect password."""
    res = requests.post(BASE_URL + "/sessions",
                        data={'email': email, "password": password})
    assert(res.status_code == 401)


def profile_unlogged() -> None:
    """Accesses the profile endpoint without logging in, expecting a 403."""
    res = requests.get(BASE_URL + '/profile')
    assert(res.status_code == 403)


def log_in(email: str, password: str) -> str:
    """Logs in with the specified email and password, returning session ID"""
    res = requests.post(BASE_URL + "/sessions",
                        data={'email': email, "password": password})
    assert(res.status_code == 200)
    assert(res.json() == {"email": email, "message": "logged in"})
    return res.cookies['session_id']


def profile_logged(session_id: str) -> None:
    """Accesses the profile endpoint with a valid session ID."""
    cookies = {'session_id': session_id}
    res = requests.get(BASE_URL + '/profile', cookies=cookies)
    assert(res.status_code == 200)


def log_out(session_id: str) -> None:
    """Logs out the user with the specified session ID."""
    cookies = {'session_id': session_id}
    res = requests.delete(BASE_URL + '/sessions', cookies=cookies)
    if res.status_code == 302:
        assert(res.url == BASE_URL)
    else:
        assert(res.status_code == 200)


def reset_password_token(email: str) -> str:
    """Requests a password reset token for the specified email."""
    res = requests.post(BASE_URL + '/reset_password', data={'email': email})
    if res.status_code == 200:
        return res.json()['reset_token']
    assert(res.status_code == 401)


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Updates the password for the specified email using the provided
    reset token and new password.
    """
    data = {'email': email, 'reset_token': reset_token,
            'new_password': new_password}
    res = requests.put(BASE_URL + '/reset_password', data=data)
    if res.status_code == 200:
        assert(res.json() == {"email": email, "message": "Password updated"})
    else:
        assert(res.status_code == 403)


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
