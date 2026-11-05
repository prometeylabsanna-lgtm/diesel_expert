from django.contrib import admin
from django.utils import timezone

from landing.admin_filters import CreatedRangeFilter, UkChoicesDropdownFilter
from landing.admin_mixins import TopFiltersMixin, mark_done
from landing.models import Lead
from unfold.admin import ModelAdmin


@admin.register(Lead)
class LeadAdmin(TopFiltersMixin, ModelAdmin):
    list_display = ("name", "phone", "service_title", "status", "sent_at")
    list_editable = ("status",)
    list_filter = (
        ("status", UkChoicesDropdownFilter),
        ("created_at", CreatedRangeFilter),
    )
    list_filter_options = {
        "status": {"label": "Статус", "horizontal": True},
        "created_at": {"label": "Надіслано", "horizontal": True},
    }
    search_fields = ("name", "phone", "service_title")
    search_help_text = "Ім’я, телефон або послуга"
    readonly_fields = ("created_at",)
    actions = (mark_done,)
    fields = ("name", "phone", "service_title", "status", "created_at")

    @admin.display(description="Надіслано", ordering="created_at")
    def sent_at(self, obj):
        return timezone.localtime(obj.created_at).strftime("%d.%m.%Y %H:%M")
