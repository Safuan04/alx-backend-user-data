#!/usr/bin/env python3
""" Auth class
"""
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """ Returns bytes that is a salted hash of the input password
    """
    salt = gensalt()
    hashed_pwd = hashpw(password.encode('utf-8'), salt)

    return hashed_pwd
