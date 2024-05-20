import jwt
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


def get_user(request):
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            # Extract the token from the Authorization header
            token = auth_header.split()[1]
            # Validate the token
            validated_token = JWTAuthentication().get_validated_token(token)
            # Set the user on the request
            user_id = validated_token.get('user_id')
        except Exception:
            pass
    else:
        user_id = None
    return user_id