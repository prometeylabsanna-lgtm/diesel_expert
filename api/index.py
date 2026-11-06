"""Vercel Python entrypoint (WSGI → serverless)."""

import os

# Vercel сам виставляє VERCEL=1; для локального `vercel dev` дублюємо безпечно.
os.environ.setdefault("VERCEL", "1")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from config.wsgi import application  # noqa: E402

app = application
