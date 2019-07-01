from django.apps import AppConfig
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy


class CityNavConfig(AppConfig):
    name = 'apps.citynav'
    verbose_name = capfirst(gettext_lazy('city navigation'))
