from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.http import JsonResponse
from api.utils.helper import get_user
from django.db import connections
from api.models import CustomUser

class JWTMiddleware(MiddlewareMixin):
    @staticmethod
    def get_email_from_user_id(user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
            return user.email
        except CustomUser.DoesNotExist:
            return None

    def process_request(self, request):
        user = get_user(request)
        if isinstance(user, JsonResponse):
            return user  # This is an error response, so return it immediately
        request.user = user

        # Check if request is from Django REST Framework
        if hasattr(request, 'query_params'):
            db_name = request.query_params.get('database')
        else:
            db_name = request.GET.get('database')

        email = self.get_email_from_user_id(user)

        # Validate the database name
        if db_name and db_name in connections.databases:
            # Switch database connection
            connections['default'] = connections[db_name]

    def process_response(self, request, response):
        return response
