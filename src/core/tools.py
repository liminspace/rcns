import threading
from debug_toolbar.middleware import DebugToolbarMiddleware
from django.conf import settings


def show_debug_toolbar(request):
    if request.META.get('REMOTE_ADDR', None) not in settings.INTERNAL_IPS and '*' not in settings.INTERNAL_IPS:
        return False
    return bool(settings.DEBUG)


def disable_debug_toolbar_for_current_request():
    DebugToolbarMiddleware.debug_toolbars.pop(threading.current_thread().ident, None)
