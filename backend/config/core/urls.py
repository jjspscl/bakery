from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from ..common import urlpatterns
import time

urlpatterns += [
    path('api/', include('apps.core.urls')),
]

if settings.DEBUG:
    from django.contrib import admin
    import debug_toolbar
    from pprint import pprint
    urlpatterns += [
        path('admin/', admin.site.urls),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
