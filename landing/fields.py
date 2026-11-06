"""Кастомні поля моделей."""

from __future__ import annotations

from django.db.models import ImageField, SlugField
from django.utils.text import slugify

from landing.image_webp import convert_upload_to_webp


class WebPImageField(ImageField):
    """ImageField з автоконвертацією нового upload → WebP."""

    def pre_save(self, model_instance, add):
        file = getattr(model_instance, self.attname)
        if file and not getattr(file, "_committed", True):
            converted = convert_upload_to_webp(file)
            if converted is not None:
                setattr(model_instance, self.attname, converted)
        return super().pre_save(model_instance, add)

    def deconstruct(self):
        name, _path, args, kwargs = super().deconstruct()
        return name, "django.db.models.ImageField", args, kwargs


class AutoSlugField(SlugField):
    """Slug з title/name; у формі лише для читання."""

    def __init__(self, *args, populate_from: str = "title", **kwargs):
        self.populate_from = populate_from
        kwargs.setdefault("max_length", 160)
        kwargs.setdefault("blank", True)
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname) or ""
        if not value:
            source = getattr(model_instance, self.populate_from, "") or ""
            value = slugify(source, allow_unicode=True)[: self.max_length]
            setattr(model_instance, self.attname, value)
        return super().pre_save(model_instance, add)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["populate_from"] = self.populate_from
        return name, path, args, kwargs
