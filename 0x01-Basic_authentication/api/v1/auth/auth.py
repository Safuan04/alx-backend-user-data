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
        return False
    

    def authorization_header(self, request=None) -> str:
        """ Authorization header
        """
        return None
    

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user
        """
        return None