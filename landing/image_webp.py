"""Конвертація завантажених зображень у WebP (без ресайзу)."""

from __future__ import annotations

import logging
from io import BytesIO
from pathlib import Path, PurePosixPath

from django.core.files.base import ContentFile
from PIL import Image, UnidentifiedImageError

logger = logging.getLogger(__name__)

WEBP_QUALITY = 88
_SKIP_EXT = {".svg", ".svgz"}
_ALREADY_WEBP = {".webp"}


def _is_animated_gif(img: Image.Image) -> bool:
    if img.format != "GIF":
        return False
    try:
        return bool(getattr(img, "is_animated", False) and img.n_frames > 1)
    except (AttributeError, ValueError):
        return False


def convert_upload_to_webp(uploaded_file, *, quality: int = WEBP_QUALITY) -> ContentFile | None:
    """Повертає ContentFile (.webp) або None, якщо конвертація не потрібна."""
    if not uploaded_file:
        return None

    name = getattr(uploaded_file, "name", "") or ""
    ext = PurePosixPath(name).suffix.lower()
    if ext in _SKIP_EXT or ext in _ALREADY_WEBP:
        return None

    raw = getattr(uploaded_file, "file", uploaded_file)
    try:
        if hasattr(raw, "seek"):
            raw.seek(0)
        img = Image.open(raw)
        img.load()
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        logger.warning("webp skip (cannot open %s): %s", name, exc)
        try:
            if hasattr(raw, "seek"):
                raw.seek(0)
        except Exception:
            pass
        return None

    if _is_animated_gif(img) or (img.format or "").upper() == "WEBP":
        try:
            if hasattr(raw, "seek"):
                raw.seek(0)
        except Exception:
            pass
        return None

    if img.mode in ("RGBA", "LA"):
        converted = img.convert("RGBA")
    elif img.mode == "P":
        converted = (
            img.convert("RGBA") if "transparency" in img.info else img.convert("RGB")
        )
    elif img.mode != "RGB":
        converted = img.convert("RGB")
    else:
        converted = img

    buf = BytesIO()
    converted.save(buf, format="WEBP", quality=quality, method=6)
    buf.seek(0)
    new_name = str(PurePosixPath(PurePosixPath(name).name).with_suffix(".webp"))
    return ContentFile(buf.read(), name=new_name)


def convert_path_to_webp(path: Path, *, quality: int = WEBP_QUALITY, delete_source: bool = True) -> Path | None:
    """Конвертує файл на диску → .webp поруч. Повертає новий шлях або None."""
    if not path.is_file():
        return None
    ext = path.suffix.lower()
    if ext in _SKIP_EXT or ext in _ALREADY_WEBP:
        return None
    try:
        img = Image.open(path)
        img.load()
    except (UnidentifiedImageError, OSError, ValueError):
        return None
    if _is_animated_gif(img):
        return None
    if img.mode in ("RGBA", "LA", "P"):
        converted = img.convert("RGBA") if img.mode != "P" or "transparency" in img.info else img.convert("RGB")
    elif img.mode != "RGB":
        converted = img.convert("RGB")
    else:
        converted = img
    dest = path.with_suffix(".webp")
    converted.save(dest, format="WEBP", quality=quality, method=6)
    if delete_source and dest != path:
        try:
            path.unlink()
        except OSError:
            pass
    return dest
