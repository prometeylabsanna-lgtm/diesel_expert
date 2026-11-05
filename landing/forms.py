import re

from django import forms
from django.core.exceptions import ValidationError

from landing.models import Service

_TAG = re.compile(r"<[^>]*>")


class LeadForm(forms.Form):
    name = forms.CharField(max_length=80, strip=True)
    phone = forms.CharField(max_length=32, strip=True)
    service = forms.CharField(max_length=200, strip=True)

    def clean_name(self):
        name = _TAG.sub("", self.cleaned_data["name"]).strip()
        if len(name) < 2:
            raise ValidationError("Вкажіть ім’я.")
        return name

    def clean_phone(self):
        digits = re.sub(r"\D", "", self.cleaned_data["phone"])
        if digits.startswith("380") and len(digits) == 12:
            normalized = digits
        elif digits.startswith("80") and len(digits) == 11:
            normalized = "3" + digits
        elif digits.startswith("0") and len(digits) == 10:
            normalized = "38" + digits
        else:
            raise ValidationError("Вкажіть номер у форматі 0XX XXX XX XX.")
        return f"+{normalized}"

    def clean_service(self):
        title = self.cleaned_data["service"]
        if not Service.objects.filter(title=title, is_published=True).exists():
            raise ValidationError("Оберіть послугу зі списку.")
        return title
