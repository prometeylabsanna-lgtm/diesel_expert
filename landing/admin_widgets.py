"""Віджети Unfold CMS: лічильник, TinyMCE, превʼю зображень."""

from django.contrib.admin.widgets import AdminTextareaWidget, AdminTextInputWidget
from django.forms import Media
from django.utils.html import format_html
from unfold.widgets import INPUT_CLASSES, TEXTAREA_CLASSES, UnfoldAdminFileFieldWidget

CMS_COUNTER_MEDIA = Media(
    js=("js/admin/cms_char_counter.js",),
    css={"all": ("css/admin/cms_char_counter.css",)},
)


def _apply_max_chars(attrs: dict, max_chars: int | None, *, hard: bool) -> dict:
    if not max_chars:
        return attrs
    attrs["data-max-chars"] = str(max_chars)
    if hard:
        attrs["maxlength"] = str(max_chars)
    return attrs


class CmsAdminTextInputWidget(AdminTextInputWidget):
    def __init__(self, attrs=None, *, max_chars: int | None = None, hard_limit: bool = True):
        attrs = dict(attrs or {})
        existing = attrs.get("class", "")
        merged = list(INPUT_CLASSES) + ["cms-countable"]
        if existing:
            merged = list(dict.fromkeys([*merged, *existing.split()]))
        attrs["class"] = " ".join(merged)
        attrs = _apply_max_chars(attrs, max_chars, hard=hard_limit)
        super().__init__(attrs=attrs)

    @property
    def media(self):
        return super().media + CMS_COUNTER_MEDIA


class CmsAdminTextareaWidget(AdminTextareaWidget):
    def __init__(self, attrs=None, *, max_chars: int | None = None, hard_limit: bool = False):
        attrs = dict(attrs or {})
        rows = attrs.pop("rows", 4)
        existing = attrs.get("class", "")
        merged = list(TEXTAREA_CLASSES) + ["cms-countable"]
        if existing:
            merged = list(dict.fromkeys([*merged, *existing.split()]))
        attrs["class"] = " ".join(merged)
        attrs["rows"] = rows
        attrs = _apply_max_chars(attrs, max_chars, hard=hard_limit)
        super().__init__(attrs=attrs)

    @property
    def media(self):
        return super().media + CMS_COUNTER_MEDIA


class CmsImageFieldWidget(UnfoldAdminFileFieldWidget):
    def __init__(
        self,
        attrs=None,
        *,
        hint: str = "",
        preview_url: str = "",
        is_icon: bool = False,
    ):
        self.hint = hint or ""
        self.preview_url = preview_url or ""
        self.is_icon = is_icon
        super().__init__(attrs=attrs)

    def render(self, name, value, attrs=None, renderer=None):
        attrs = {} if attrs is None else dict(attrs)
        if attrs.get("accept") == "image/*":
            attrs["accept"] = "image/png,image/jpeg,image/webp"
        html = super().render(name, value, attrs=attrs, renderer=renderer)
        preview = ""
        url = self.preview_url
        if not url and value and hasattr(value, "url"):
            try:
                url = value.url
            except Exception:
                url = ""
        if url:
            mod = " cms-img-preview--icon" if self.is_icon else ""
            preview = format_html(
                '<div class="cms-img-preview{}">'
                '<img src="{}" alt="" loading="lazy" decoding="async">'
                "</div>",
                mod,
                url,
            )
        hint = ""
        if self.hint:
            hint = format_html('<p class="cms-img-hint">{}</p>', self.hint)
        return format_html("{}{}{}", preview, hint, html)

    class Media:
        css = {"all": ("css/admin/cms_preview.css",)}


class CmsTinyMCEWidget(AdminTextareaWidget):
    def __init__(self, attrs=None, *, max_chars: int | None = None, hard_limit: bool = False):
        attrs = dict(attrs or {})
        rows = attrs.pop("rows", 14)
        existing = attrs.get("class", "")
        merged = list(TEXTAREA_CLASSES) + ["cms-tinymce", "cms-countable"]
        if existing:
            merged = list(dict.fromkeys([*merged, *existing.split()]))
        attrs["class"] = " ".join(merged)
        attrs["rows"] = rows
        attrs = _apply_max_chars(attrs, max_chars, hard=hard_limit)
        super().__init__(attrs=attrs)

    class Media:
        js = (
            "https://cdn.jsdelivr.net/npm/tinymce@7.6.1/tinymce.min.js",
            "js/admin/cms_tinymce.js",
            "js/admin/cms_char_counter.js",
        )
        css = {
            "all": (
                "css/admin/cms_tinymce.css",
                "css/admin/cms_char_counter.css",
            ),
        }
