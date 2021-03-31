#!/usr/bin/env python3
"""
Manage the API authentication.
"""
from api.v1.auth.auth import Auth
from base64 import b64decode


class BasicAuth(Auth):
    """Inherits from Auth"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract"""
        if authorization_header is None:
            return None

        if type(authorization_header) != str:
            return None

        if authorization_header[:6] == 'Basic ':
            return authorization_header[6:]
        else:
            return None

    def decode_base64_authorization_header(
                                            self,
                                            base64_authorization_header: str
                                            ) -> str:
        """Decoded value of a Base64 string"""
        if base64_authorization_header is None:
            return None

        if type(base64_authorization_header) is not str:
            return None

        try:
            return b64decode(base64_authorization_header).decode('utf-8')
        except Exception:
            return None