#!/usr/bin/env python3
""" Creating the class Auth
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ auth requirement
        """
        if not path:
            return True

        if not path.endswith('/'):
            path += '/'

        if not excluded_paths or excluded_paths == []:
            return True

        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """ Authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user
        """
        return None
