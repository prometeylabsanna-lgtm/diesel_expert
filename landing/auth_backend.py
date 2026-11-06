"""Стійка auth для Vercel-демо: /tmp SQLite може бути порожнім на cold start."""

from __future__ import annotations

import logging
import os

from django.contrib.auth.backends import ModelBackend

logger = logging.getLogger(__name__)


class VercelResilientAuthBackend(ModelBackend):
    """Перед authenticate/get_user гарантує наявність demo-superuser у SQLite."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        self._ensure_demo()
        return super().authenticate(
            request, username=username, password=password, **kwargs
        )

    def get_user(self, user_id):
        self._ensure_demo()
        user = super().get_user(user_id)
        if user is not None:
            return user
        if not os.environ.get("VERCEL"):
            return None
        from django.contrib.auth import get_user_model

        from landing.bootstrap_vercel import DEMO_USERNAME

        return (
            get_user_model()
            .objects.filter(username=DEMO_USERNAME, is_active=True)
            .first()
        )

    def _ensure_demo(self) -> None:
        if not os.environ.get("VERCEL"):
            return
        try:
            from landing.bootstrap_vercel import ensure_demo_superuser

            ensure_demo_superuser()
        except Exception:
            logger.exception("ensure_demo_superuser during auth failed; full bootstrap")
            try:
                from landing.bootstrap_vercel import bootstrap_vercel_demo

                bootstrap_vercel_demo()
            except Exception:
                logger.exception("bootstrap_vercel_demo during auth failed")
