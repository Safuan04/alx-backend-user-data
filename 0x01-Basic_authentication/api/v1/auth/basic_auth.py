#!/usr/bin/env python3
""" Creating the BasicAuth class
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ BasicAuth class
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ Extracting the base64 authorization header
        """
