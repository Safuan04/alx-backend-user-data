#!/usr/bin/env python3
""" Creating the SessionAuth class
"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """ SessionAuth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """  creates a Session ID for a user_id
        """
        if not user_id:
            return None
        if not isinstance(user_id, str):
            return None

        self.id = str(uuid.uuid4())
        self.user_id_by_session_id[self.id] = user_id
        return self.id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ returns a User ID based on a Session ID
        """
        if not session_id:
            return None
        if not isinstance(session_id, str):
            return None
        value = self.user_id_by_session_id.get(session_id)
        return value

    def current_user(self, request=None):
        """ returns a User instance based on a cookie value
        """
        user = None
        cookie_value = self.session_cookie(request)
        if cookie_value:
            user_id = self.user_id_for_session_id(cookie_value)
            if user_id:
                user = User.get(user_id)

        return user
