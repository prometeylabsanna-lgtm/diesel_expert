"""Middleware для Vercel-демо (ефемерний SQLite)."""

from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)


class VercelEnsureDemoMiddleware:
    """Перед admin-auth гарантує migrate + demo-user у /tmp SQLite."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if os.environ.get("VERCEL") and request.path.startswith("/admin"):
            from django.db.utils import OperationalError

            from landing.bootstrap_vercel import (
                bootstrap_vercel_demo,
                ensure_demo_superuser,
            )

            try:
                ensure_demo_superuser()
            except OperationalError:
                # Порожній /tmp після cold start — повний migrate + seed
                try:
                    bootstrap_vercel_demo()
                except Exception:
                    logger.exception("vercel bootstrap on admin request failed")
            except Exception:
                logger.exception("vercel ensure on admin request failed")
        return self.get_response(request)
