"""Безпечні кольори оформлення для публічного CSS."""

import re

from landing.models.settings import (
    COLOR_ACCENT_DEFAULT,
    COLOR_BG_DEFAULT,
    COLOR_HIGHLIGHT_DEFAULT,
    COLOR_TEXT_DEFAULT,
)

_HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")


def _pick(value, fallback):
    text = (value or "").strip()
    if _HEX.fullmatch(text):
        return text.lower()
    return fallback


def accent_soft(hex_color):
    value = hex_color.lstrip("#")
    red = int(value[0:2], 16)
    green = int(value[2:4], 16)
    blue = int(value[4:6], 16)
    return f"rgba({red}, {green}, {blue}, 0.12)"


def public_colors(site):
    highlight = _pick(getattr(site, "color_highlight", ""), COLOR_HIGHLIGHT_DEFAULT)
    return {
        "color_bg": _pick(getattr(site, "color_bg", ""), COLOR_BG_DEFAULT),
        "color_text": _pick(getattr(site, "color_text", ""), COLOR_TEXT_DEFAULT),
        "color_highlight": highlight,
        "color_accent": _pick(getattr(site, "color_accent", ""), COLOR_ACCENT_DEFAULT),
        "color_accent_soft": accent_soft(highlight),
    }
