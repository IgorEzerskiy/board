from django.utils import timezone
from board import settings
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication


class TokenExpiredAuthentication(TokenAuthentication):
    def authenticate(self, request):
        try:
            user, token = super().authenticate(request=request)
        except TypeError:
            return None

        if (timezone.now() - token.created).seconds > settings.TOKEN_LIFETIME:
            token.delete()
            raise exceptions.AuthenticationFailed(
                f'Token was created more the {settings.TOKEN_LIFETIME} seconds ago.'
            )
        return user, token

