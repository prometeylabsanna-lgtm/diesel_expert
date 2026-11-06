"""Демо-бутстрап для Vercel (ефемерний SQLite в /tmp). Не для прод з постійною БД."""

from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

DEMO_USERNAME = "admin"
DEMO_PASSWORD = "admin"
DEMO_EMAIL = "admin@diesel-expert.local"
# Фіксований hash (salt ≥128 bit entropy) → Django не робить rehash на login,
# тож cookie-сесія (_auth_user_hash) стабільна між cold start на Vercel.
DEMO_PASSWORD_HASH = (
    "pbkdf2_sha256$1000000$DieselExpertDemoFixedSalt128bitOK$"
    "jVuZQyljL1ymoormgakCq0wUFswDn0sp01LbSIz4hHs="
)


def _demo_password_hash() -> str:
    return DEMO_PASSWORD_HASH


def ensure_demo_superuser() -> None:
    if not os.environ.get("VERCEL"):
        return
    from django.contrib.auth import get_user_model

    user_model = get_user_model()
    desired_hash = _demo_password_hash()
    user, created = user_model.objects.get_or_create(
        username=DEMO_USERNAME,
        defaults={
            "email": DEMO_EMAIL,
            "is_staff": True,
            "is_superuser": True,
            "is_active": True,
            "password": desired_hash,
        },
    )
    changed = created
    if not user.is_staff or not user.is_superuser or not user.is_active:
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        changed = True
    # Не перезаписувати password, якщо admin/admin вже валідний:
    # Django після login може зробити rehash (інший salt) — скидання
    # до DEMO_PASSWORD_HASH інвалідує _auth_user_hash і кидає на login.
    if not user.check_password(DEMO_PASSWORD):
        user.password = desired_hash
        changed = True
    if not user.email:
        user.email = DEMO_EMAIL
        changed = True
    if changed:
        user.save()
    logger.info(
        "vercel demo superuser %s (%s)",
        DEMO_USERNAME,
        "created" if created else ("updated" if changed else "ok"),
    )


def bootstrap_vercel_demo() -> None:
    if not os.environ.get("VERCEL"):
        return
    from django.core.management import call_command

    try:
        call_command("migrate", interactive=False, run_syncdb=True, verbosity=0)
    except Exception:
        logger.exception("vercel migrate failed")

    try:
        ensure_demo_superuser()
    except Exception:
        logger.exception("vercel demo superuser failed")

    try:
        from landing.seed import seed_if_empty

        seed_if_empty()
    except Exception:
        logger.exception("vercel seed_if_empty failed")
