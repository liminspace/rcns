# noinspection PyUnresolvedReferences
from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.citynav.urls')),
]


if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from django.views.generic.base import RedirectView

    urlpatterns.extend([
        path('__debug__/', include(debug_toolbar.urls)),
        path(
            'favicon.ico',
            RedirectView.as_view(url=f'{settings.STATIC_URL}img/favicon.ico'),
            name='favicon_ico'
        ),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True))
