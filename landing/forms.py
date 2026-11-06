import re

from django import forms
from django.core.exceptions import ValidationError

from landing.models import Service

_TAG = re.compile(r"<[^>]*>")
_NAME_OK = re.compile(r"^[A-Za-zА-Яа-яЁёІіЇїЄєҐґ'\u2019\u02BC\-\s]+$")
_HAS_LETTER = re.compile(r"[A-Za-zА-Яа-яЁёІіЇїЄєҐґ]")
_PHONE_ALLOWED = re.compile(r"^[\d\s+\-()]+$")


class LeadForm(forms.Form):
    name = forms.CharField(max_length=80, strip=True)
    phone = forms.CharField(max_length=32, strip=True)
    service = forms.CharField(max_length=200, strip=True)

    def clean_name(self):
        name = _TAG.sub("", self.cleaned_data["name"]).strip()
        if len(name) < 2:
            raise ValidationError("Вкажіть ім’я (мінімум 2 символи).")
        if not _NAME_OK.match(name) or not _HAS_LETTER.search(name):
            raise ValidationError(
                "Ім’я може містити лише літери, пробіл, дефіс або апостроф."
            )
        return name

    def clean_phone(self):
        raw = (self.cleaned_data["phone"] or "").strip()
        if _HAS_LETTER.search(raw):
            raise ValidationError("У номері не можна вводити літери.")
        if raw and not _PHONE_ALLOWED.match(raw):
            raise ValidationError("У номері дозволені лише цифри та +.")
        digits = re.sub(r"\D", "", raw)
        if digits.startswith("380") and len(digits) == 12:
            normalized = digits
        elif digits.startswith("80") and len(digits) == 11:
            normalized = "3" + digits
        elif digits.startswith("0") and len(digits) == 10:
            normalized = "38" + digits
        else:
            raise ValidationError(
                "Вкажіть український номер: +380XXXXXXXXX (13 символів)."
            )
        phone = f"+{normalized}"
        if len(phone) != 13:
            raise ValidationError(
                "Вкажіть український номер: +380XXXXXXXXX (13 символів)."
            )
        return phone

    def clean_service(self):
        title = self.cleaned_data["service"]
        if not Service.objects.filter(title=title, is_published=True).exists():
            raise ValidationError("Оберіть послугу зі списку.")
        return title
