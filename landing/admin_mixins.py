from django.contrib import admin
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html

from unfold.admin import ModelAdmin

from landing.admin_filters import PublishedFilter
from landing.admin_guidelines import (
    TINYMCE_FIELDS,
    help_for_field,
    image_profile_for_field,
    text_limit_for_field,
)
from landing.admin_widgets import (
    CmsAdminTextInputWidget,
    CmsAdminTextareaWidget,
    CmsImageFieldWidget,
    CmsTinyMCEWidget,
)
from landing.images import public_url


class TopFiltersMixin:
    list_filter_sheet = False


class CmsWidgetsMixin:
    """Лічильники, TinyMCE, підказки та превʼю зображень."""

    readonly_slug_fields = ("slug", "modifier")

    def get_readonly_fields(self, request, obj=None):
        base = list(super().get_readonly_fields(request, obj))
        for name in self.readonly_slug_fields:
            if hasattr(self.model, name) and name not in base:
                base.append(name)
        return base

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        name = db_field.name
        help_text = help_for_field(name)
        if help_text and not kwargs.get("help_text"):
            kwargs["help_text"] = help_text

        if isinstance(db_field, models.ImageField):
            preview = ""
            obj = getattr(request, "_cms_admin_obj", None)
            if obj is not None:
                file_val = getattr(obj, name, None)
                static_name = f"{name}_static" if not name.endswith("_static") else ""
                static_path = getattr(obj, static_name, "") if static_name else ""
                if name.endswith("_static"):
                    static_path = getattr(obj, name, "") or ""
                    preview = public_url(None, static_path) if static_path else ""
                else:
                    preview = public_url(
                        file_val,
                        static_path or getattr(obj, f"{name}_static", ""),
                    )
            is_icon = "icon" in name or name == "logo"
            kwargs["widget"] = CmsImageFieldWidget(
                hint=image_profile_for_field(name).hint,
                preview_url=preview,
                is_icon=is_icon,
            )
            return db_field.formfield(**kwargs)

        limit = text_limit_for_field(name)
        max_chars = limit.max_chars if limit else None
        hard = bool(limit and not limit.soft)

        if name in TINYMCE_FIELDS or (
            isinstance(db_field, models.TextField)
            and name.endswith("_body")
        ):
            kwargs["widget"] = CmsTinyMCEWidget(max_chars=max_chars, hard_limit=False)
            return db_field.formfield(**kwargs)

        if isinstance(db_field, models.TextField):
            kwargs["widget"] = CmsAdminTextareaWidget(
                max_chars=max_chars,
                hard_limit=hard,
                attrs={"rows": 4},
            )
            return db_field.formfield(**kwargs)

        if isinstance(db_field, (models.CharField, models.SlugField)) and name not in self.readonly_slug_fields:
            kwargs["widget"] = CmsAdminTextInputWidget(
                max_chars=max_chars or getattr(db_field, "max_length", None),
                hard_limit=hard if limit else True,
            )
            return db_field.formfield(**kwargs)

        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def get_form(self, request, obj=None, change=False, **kwargs):
        request._cms_admin_obj = obj
        return super().get_form(request, obj, change=change, **kwargs)

    @admin.display(description="Превʼю")
    def preview_thumb(self, obj):
        url = ""
        for attr, static_attr in (
            ("image", "image_static"),
            ("icon", "icon_static"),
            ("logo", "logo_static"),
            ("hero_image", "hero_image_static"),
            ("promo_image", "promo_image_static"),
        ):
            if hasattr(obj, attr):
                url = public_url(getattr(obj, attr, None), getattr(obj, static_attr, ""))
                if url:
                    break
        if not url:
            return "—"
        model_fields = {f.name for f in obj._meta.get_fields()}
        uses_icon = "icon" in model_fields or "icon_static" in model_fields
        uses_photo = "image" in model_fields or "hero_image" in model_fields
        if uses_icon and not uses_photo:
            return format_html(
                '<span class="de-thumb de-thumb--icon">'
                '<img src="{}" alt="" width="40" height="40" loading="lazy">'
                "</span>",
                url,
            )
        return format_html(
            '<span class="de-thumb">'
            '<img src="{}" alt="" width="56" height="40" loading="lazy">'
            "</span>",
            url,
        )


class PublishedAdmin(CmsWidgetsMixin, TopFiltersMixin, ModelAdmin):
    list_editable = ("sort", "is_published")
    list_filter = (PublishedFilter,)
    list_filter_options = {
        "is_published": {"label": "На сайті", "horizontal": True},
    }


class SingletonAdmin(CmsWidgetsMixin, ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        from landing.seed import seed_if_empty

        seed_if_empty()
        url = reverse(
            f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change",
            args=[1],
        )
        return redirect(url)


@admin.action(description="Позначити опрацьованими")
def mark_done(modeladmin, request, queryset):
    from landing.models import Lead

    queryset.update(status=Lead.Status.DONE)
