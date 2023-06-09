from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin
from board import settings
import datetime


class LogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_staff or not request.user.is_superuser:
            now = datetime.datetime.now()
            last_action_not_decoded = request.session.get('last_action')
            if last_action_not_decoded:
                last_action = datetime.datetime.strptime(last_action_not_decoded, "%H-%M-%S %d/%m/%y")
                if (now - last_action).seconds > settings.ALLOWED_TIME_OF_USER_INACTIVITY:
                    logout(request)
            request.session['last_action'] = datetime.datetime.now().strftime("%H-%M-%S %d/%m/%y")
