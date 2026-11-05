from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from unfold.admin import ModelAdmin

from landing.admin_filters import PublishedFilter


class TopFiltersMixin:
    list_filter_sheet = False


class PublishedAdmin(TopFiltersMixin, ModelAdmin):
    list_editable = ("sort", "is_published")
    list_filter = (PublishedFilter,)
    list_filter_options = {
        "is_published": {"label": "На сайті", "horizontal": True},
    }


class SingletonAdmin(ModelAdmin):
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
