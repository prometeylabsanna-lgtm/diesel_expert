from collections.abc import Iterator

from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.core.validators import EMPTY_VALUES
from django.db.models import DateTimeField, QuerySet
from django.forms import ValidationError
from django.http import HttpRequest

from unfold.contrib.filters.admin import ChoicesDropdownFilter, DropdownFilter, RangeDateFilter
from unfold.contrib.filters.forms import RangeDateForm
from unfold.utils import parse_date_str


class UkChoicesDropdownFilter(ChoicesDropdownFilter):
    all_option = ["", "Усі"]

    def choices(self, changelist: ChangeList) -> Iterator:
        choices = [self.all_option]
        for choice in self.field.flatchoices:
            choices.append(choice)
        yield {
            "form": self.form_class(
                label=str(self.title),
                name=self.lookup_kwarg,
                choices=choices,
                data={self.lookup_kwarg: self.value()},
                multiple=False,
            ),
        }


class PublishedFilter(DropdownFilter):
    title = "На сайті"
    parameter_name = "is_published"
    all_option = ["", "Усі"]

    def lookups(self, request, model_admin):
        return (("1", "Так"), ("0", "Ні"))

    def queryset(self, request, queryset):
        if self.value() == "1":
            return queryset.filter(is_published=True)
        if self.value() == "0":
            return queryset.filter(is_published=False)
        return queryset

    def choices(self, changelist: ChangeList) -> Iterator:
        choices = [self.all_option, *self.lookup_choices]
        yield {
            "form": self.form_class(
                label=str(self.title),
                name=self.parameter_name,
                choices=choices,
                data={self.parameter_name: self.value()},
                multiple=False,
            ),
        }


class UkRangeDateForm(RangeDateForm):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.fields[f"{name}_from"].widget.attrs["placeholder"] = "Від"
        self.fields[f"{name}_to"].widget.attrs["placeholder"] = "До"


class CreatedRangeFilter(RangeDateFilter):
    form_class = UkRangeDateForm

    def __init__(self, field, request, params, model, model_admin, field_path):
        admin.FieldListFilter.__init__(
            self, field, request, params, model, model_admin, field_path
        )
        if not isinstance(field, DateTimeField):
            raise TypeError("CreatedRangeFilter працює лише з датою й часом.")
        self.request = request
        if self.parameter_name is None:
            self.parameter_name = self.field_path
        self._take(params, "_from")
        self._take(params, "_to")

    def _take(self, params, suffix):
        key = self.parameter_name + suffix
        if key not in params:
            return
        value = params.pop(key)
        value = value[0] if isinstance(value, list) else value
        if value not in EMPTY_VALUES:
            self.used_parameters[key] = value

    def queryset(self, request: HttpRequest, queryset: QuerySet):
        filters = {}
        value_from = self.used_parameters.get(f"{self.parameter_name}_from")
        value_to = self.used_parameters.get(f"{self.parameter_name}_to")
        if value_from not in EMPTY_VALUES and isinstance(value_from, str):
            filters[f"{self.parameter_name}__date__gte"] = parse_date_str(value_from)
        if value_to not in EMPTY_VALUES and isinstance(value_to, str):
            filters[f"{self.parameter_name}__date__lte"] = parse_date_str(value_to)
        try:
            return queryset.filter(**filters)
        except (ValueError, ValidationError):
            return queryset.none()
