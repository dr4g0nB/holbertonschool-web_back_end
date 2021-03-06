#!/usr/bin/env python3
"""
Manage the API authentication.
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from typing import TypeVar
from models.user import User


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

    def extract_user_credentials(
                                  self,
                                  decoded_base64_authorization_header: str
                                  ) -> (str, str):
        """Return
            - User email and password
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if type(decoded_base64_authorization_header) is not str:
            return None, None

        if ':' in decoded_base64_authorization_header:
            uno = decoded_base64_authorization_header.split(sep=':')
            return tuple(uno)
        else:
            return None, None

    def user_object_from_credentials(
                                      self,
                                      user_email: str,
                                      user_pwd: str
                                    ) -> TypeVar('User'):
        """Return
            - User instance based on his email and password.
        """
        if user_email is None or user_pwd is None or not isinstance(
                user_email, str) or not isinstance(user_pwd, str):
            return None

        users = User.search({'email': user_email})

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Overloads Auth and retrieves the User instance for a request"""
        au_h = self.authorization_header(request)
        extract = self.extract_base64_authorization_header(au_h)
        decode = self.decode_base64_authorization_header(extract)
        user = self.extract_user_credentials(decode)
        return self.user_object_from_credentials(user[0], user[1])
