from django.apps import AppConfig
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy


class UserauthConfig(AppConfig):
    name = 'apps.userauth'
    verbose_name = capfirst(gettext_lazy('users'))
