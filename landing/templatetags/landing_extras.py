import html
import re

from django import template
from django.template.defaultfilters import linebreaks
from django.utils.safestring import mark_safe

register = template.Library()

_HTML = re.compile(r"<[a-z][\s\S]*>", re.I)
_ESCAPED_HTML = re.compile(r"&lt;/[a-z]+&gt;|&lt;[a-z]+(?:\s[^&]*)?&gt;", re.I)


@register.filter(name="richtext", is_safe=True)
def richtext(value):
    """HTML з TinyMCE як є; екранований HTML — розкодувати; текст — з переносами."""
    text = value or ""
    if _ESCAPED_HTML.search(text) and not _HTML.search(text):
        text = html.unescape(text)
    if _HTML.search(text):
        return mark_safe(text)
    # linebreaks() у поточному Django може повернути звичайний str — фіксуємо SafeString
    return mark_safe(linebreaks(text))
