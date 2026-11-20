"""Згода на cookie: cookie браузера + безпечний redirect."""

from __future__ import annotations

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

CONSENT_COOKIE = "cookie_consent"
STORAGE_KEY = "de_cookie_consent"
ACCEPTED = "accepted"
DECLINED = "declined"
CHOICES = frozenset({ACCEPTED, DECLINED})
MAX_AGE = 60 * 60 * 24 * 365


def has_consent_choice(request) -> bool:
    return (request.COOKIES.get(CONSENT_COOKIE) or "") in CHOICES


def set_consent_cookie(response: HttpResponse, choice: str) -> None:
    response.set_cookie(
        CONSENT_COOKIE,
        choice,
        max_age=MAX_AGE,
        path="/",
        samesite="Lax",
        secure=not settings.DEBUG,
        httponly=True,
    )


def _safe_next(request) -> str:
    candidate = (request.POST.get("next") or "").strip() or "/"
    if candidate.startswith("//") or "\\" in candidate:
        return "/"
    if url_has_allowed_host_and_scheme(
        candidate,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return candidate
    return "/"


@require_POST
def cookie_consent(request):
    choice = (request.POST.get("choice") or "").strip()
    if choice not in CHOICES:
        return HttpResponse(status=400)
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        response = HttpResponse(status=204)
    else:
        response = redirect(_safe_next(request))
    set_consent_cookie(response, choice)
    return response
