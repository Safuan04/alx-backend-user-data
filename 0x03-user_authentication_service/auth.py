#!/usr/bin/env python3
""" Auth class
"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """ Returns bytes that is a salted hash of the input password
    """
    salt = gensalt()
    hashed_pwd = hashpw(password.encode('utf-8'), salt)

    return hashed_pwd


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register user if its not already exists
        """
        try:
            if self._db.find_user_by(email=email) is not None:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        hashed_pwd = _hash_password(password)
        saved_usr = self._db.add_user(email, hashed_pwd)

        return saved_usr

    def valid_login(self, email: str, password: str) -> bool:
        """ Credentials validation
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        return checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """ find the user corresponding to the email
        -   generate a new UUID and store it in the database
        -   as the users session_id, then return the session ID."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id


def _generate_uuid() -> str:
    """ Generate an UUID
    """
    return str(uuid.uuid4())
