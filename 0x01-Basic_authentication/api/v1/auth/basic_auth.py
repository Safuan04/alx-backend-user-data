#!/usr/bin/env python3
""" Creating the BasicAuth class
"""
from api.v1.auth.auth import Auth
import base64
from typing import Tuple


class BasicAuth(Auth):
    """ BasicAuth class
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ Extracting the base64 authorization header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        else:
            return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Decoding base64 authorization header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            base64.b64decode(base64_authorization_header)
        except ValueError:
            return None
        decoded_value = base64.b64decode(base64_authorization_header)
        utf8_decoded_value = decoded_value.decode('utf-8')
        return utf8_decoded_value

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """ Extraction users credentials
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return (email, password)
