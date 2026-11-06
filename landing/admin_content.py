from django.contrib import admin

from unfold.admin import TabularInline

from landing.admin_mixins import PublishedAdmin
from landing.models import (
    Advantage,
    FaqItem,
    HeroBadge,
    HeroCard,
    MailStep,
    Review,
    Service,
    ServicePrice,
    WorkPhoto,
)


class ServicePriceInline(TabularInline):
    model = ServicePrice
    extra = 0
    fields = ("label", "short", "value", "sort")


@admin.register(Advantage)
class AdvantageAdmin(PublishedAdmin):
    list_display = ("preview_thumb", "title", "sort", "is_published")
    list_display_links = ("preview_thumb", "title")
    search_fields = ("title", "text")
    search_help_text = "Заголовок або текст"
    fields = ("title", "text", "icon", "icon_static", "sort", "is_published")


@admin.register(HeroCard)
class HeroCardAdmin(PublishedAdmin):
    list_display = ("title", "modifier", "sort", "is_published")
    search_fields = ("title",)
    search_help_text = "Назва напрямку"
    fields = ("title", "modifier", "url", "image_static", "sort", "is_published")


@admin.register(HeroBadge)
class HeroBadgeAdmin(PublishedAdmin):
    list_display = ("preview_thumb", "text", "sort", "is_published")
    list_display_links = ("preview_thumb", "text")
    search_fields = ("text",)
    search_help_text = "Текст плашки"
    fields = ("text", "icon", "icon_static", "sort", "is_published")


@admin.register(Service)
class ServiceAdmin(PublishedAdmin):
    list_display = ("preview_thumb", "title", "slug", "sort", "is_published")
    list_display_links = ("preview_thumb", "title")
    search_fields = ("title", "slug")
    search_help_text = "Назва послуги"
    inlines = (ServicePriceInline,)
    fields = (
        "title",
        "slug",
        "bullets",
        "image",
        "image_static",
        "wide",
        "mobile_extra",
        "sort",
        "is_published",
    )


@admin.register(MailStep)
class MailStepAdmin(PublishedAdmin):
    list_display = ("num", "title", "sort", "is_published")
    search_fields = ("title", "text")
    search_help_text = "Заголовок або текст"
    fields = ("num", "title", "text", "sort", "is_published")


@admin.register(Review)
class ReviewAdmin(PublishedAdmin):
    list_display = ("name", "sort", "is_published")
    search_fields = ("name", "text")
    search_help_text = "Ім’я або текст"
    fields = ("name", "text", "sort", "is_published")


@admin.register(WorkPhoto)
class WorkPhotoAdmin(PublishedAdmin):
    list_display = ("preview_thumb", "alt", "sort", "is_published")
    list_display_links = ("preview_thumb", "alt")
    search_fields = ("alt",)
    search_help_text = "Підпис"
    fields = ("image", "image_static", "alt", "sort", "is_published")


@admin.register(FaqItem)
class FaqItemAdmin(PublishedAdmin):
    list_display = ("question", "sort", "is_published")
    search_fields = ("question", "answer")
    search_help_text = "Питання або відповідь"
    fields = ("question", "answer", "sort", "is_published")
