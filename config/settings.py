import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-only-diesel-expert-layout",
)
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = [
    host
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
    if host
]

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.forms",
    "landing",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "uk"
TIME_ZONE = "Europe/Kyiv"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "noreply@diesel-expert.local"

UNFOLD = {
    "SITE_TITLE": "Diesel Expert",
    "SITE_HEADER": "Diesel Expert",
    "SITE_URL": "/",
    "SITE_SYMBOL": "settings",
    "SHOW_HISTORY": True,
    "SITE_LOGO": {
        "light": "landing.unfold_nav.admin_logo",
        "dark": "landing.unfold_nav.admin_logo",
    },
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "any",
            "type": "image/x-icon",
            "href": "landing.unfold_nav.admin_favicon_ico",
        },
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/png",
            "href": "landing.unfold_nav.admin_favicon_32",
        },
        {
            "rel": "icon",
            "sizes": "48x48",
            "type": "image/png",
            "href": "landing.unfold_nav.admin_favicon_48",
        },
        {
            "rel": "apple-touch-icon",
            "sizes": "180x180",
            "type": "image/png",
            "href": "landing.unfold_nav.admin_apple_touch",
        },
    ],
    "STYLES": ["landing.unfold_nav.admin_style"],
    # Світла: білий + зелений; темна: чорний + зелений (accent #3D9E0E ≈ brand)
    "COLORS": {
        "primary": {
            "50": "oklch(97% 0.05 142)",
            "100": "oklch(93% 0.09 142)",
            "200": "oklch(88% 0.14 142)",
            "300": "oklch(80% 0.18 142)",
            "400": "oklch(72% 0.2 142)",
            "500": "oklch(62% 0.2 142)",
            "600": "oklch(52% 0.17 142)",
            "700": "oklch(44% 0.14 142)",
            "800": "oklch(36% 0.11 142)",
            "900": "oklch(28% 0.08 142)",
            "950": "oklch(20% 0.05 142)",
        },
        "base": {
            "50": "oklch(99% 0.005 142)",
            "100": "oklch(97% 0.008 142)",
            "200": "oklch(93% 0.01 142)",
            "300": "oklch(87% 0.012 142)",
            "400": "oklch(70% 0.015 142)",
            "500": "oklch(55% 0.015 142)",
            "600": "oklch(42% 0.012 142)",
            "700": "oklch(30% 0.01 142)",
            "800": "oklch(20% 0.008 142)",
            "900": "oklch(12% 0.005 142)",
            "950": "oklch(6% 0.003 142)",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": "landing.unfold_nav.navigation",
    },
}
