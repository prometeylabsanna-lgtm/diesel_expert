import os
import re

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("landing.urls")),
]

# django.conf.urls.static.static() при DEBUG=False повертає [] —
# на Vercel media в /tmp треба віддавати завжди.
if settings.DEBUG or os.environ.get("VERCEL"):
    media_url = settings.MEDIA_URL if settings.MEDIA_URL.endswith("/") else f"{settings.MEDIA_URL}/"
    urlpatterns += [
        re_path(
            r"^%s(?P<path>.*)$" % re.escape(media_url.lstrip("/")),
            serve,
            {"document_root": str(settings.MEDIA_ROOT)},
        ),
    ]

if settings.DEBUG and not os.environ.get("VERCEL"):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
