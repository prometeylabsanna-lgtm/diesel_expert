"""Vercel Python entrypoint (WSGI → serverless)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Корінь репозиторію (батько /api)
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.chdir(ROOT)

# Vercel сам виставляє VERCEL=1
os.environ.setdefault("VERCEL", "1")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()

# TODO(prod / DigitalOcean): прибрати bootstrap лише для Vercel-демо
if os.environ.get("VERCEL"):
    try:
        from landing.bootstrap_vercel import bootstrap_vercel_demo

        bootstrap_vercel_demo()
    except Exception:
        pass

app = application
