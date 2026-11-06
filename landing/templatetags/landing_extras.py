import re

from django import template
from django.template.defaultfilters import linebreaks
from django.utils.safestring import mark_safe

register = template.Library()

_HTML = re.compile(r"<[a-z][\s\S]*>", re.I)


@register.filter(name="richtext")
def richtext(value):
    """HTML з TinyMCE як є; звичайний текст — з переносами рядків."""
    text = value or ""
    if _HTML.search(text):
        return mark_safe(text)
    return linebreaks(text)
