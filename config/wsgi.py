import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()

# TODO(prod / DigitalOcean): прибрати — auto-migrate + seed + demo admin лише для Vercel (/tmp SQLite)
if os.environ.get("VERCEL"):
    try:
        from landing.bootstrap_vercel import bootstrap_vercel_demo

        bootstrap_vercel_demo()
    except Exception:
        pass
