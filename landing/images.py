import os

from django.core.exceptions import ValidationError
from django.templatetags.static import static

_RASTER = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
_MAX_BYTES = 8 * 1024 * 1024


def validate_raster(uploaded):
    ext = os.path.splitext(getattr(uploaded, "name", ""))[1].lower()
    if ext not in _RASTER:
        raise ValidationError("Дозволені формати: jpg, png, webp, gif.")
    size = getattr(uploaded, "size", 0) or 0
    if size > _MAX_BYTES:
        raise ValidationError("Файл більший за 8 МБ.")


def public_url(uploaded, static_path):
    name = getattr(uploaded, "name", "") or ""
    if name:
        try:
            if uploaded.storage.exists(name):
                return uploaded.url
        except Exception:
            pass
    if static_path:
        return static(static_path)
    return ""
