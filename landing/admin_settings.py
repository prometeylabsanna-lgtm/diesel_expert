from django.contrib import admin

from landing.admin_mixins import SingletonAdmin
from landing.models import (
    BookingSettings,
    ContactsSettings,
    HeroSettings,
    LegalSettings,
    SectionSettings,
)

_NOTIFY = (
    "Сповіщення",
    {"fields": ("notify_email", "telegram_bot_token", "telegram_chat_id")},
)


@admin.register(ContactsSettings)
class ContactsSettingsAdmin(SingletonAdmin):
    fieldsets = (
        (
            "Контакти",
            {"fields": ("phone", "address_line_1", "address_line_2", "schedule")},
        ),
        ("Логотип", {"fields": ("logo", "logo_static")}),
        ("Кнопки", {"fields": ("cta_service", "cta_diagnostics")}),
        ("Підвал", {"fields": ("copyright", "design_credit")}),
        _NOTIFY,
    )


@admin.register(HeroSettings)
class HeroSettingsAdmin(SingletonAdmin):
    fieldsets = (
        (
            "Пропозиція",
            {
                "fields": (
                    "hero_title",
                    "hero_primary_cta",
                    "hero_secondary_cta",
                    "hero_secondary_url",
                )
            },
        ),
        ("Фон", {"fields": ("hero_image", "hero_image_static")}),
    )


@admin.register(SectionSettings)
class SectionSettingsAdmin(SingletonAdmin):
    fieldsets = (
        ("Переваги", {"fields": ("advantages_title",)}),
        (
            "Послуги",
            {"fields": ("services_title", "services_lead", "services_more_label")},
        ),
        (
            "Нова пошта",
            {
                "fields": (
                    "promo_title",
                    "promo_lead",
                    "promo_text",
                    "promo_cta",
                    "promo_image",
                    "promo_image_static",
                )
            },
        ),
        ("Інші заголовки", {"fields": ("steps_title", "reviews_title", "works_title")}),
    )


@admin.register(BookingSettings)
class BookingSettingsAdmin(SingletonAdmin):
    fieldsets = (
        (
            "Форма",
            {
                "fields": (
                    "booking_title",
                    "booking_lead",
                    "booking_name_placeholder",
                    "booking_phone_placeholder",
                    "booking_service_placeholder",
                    "booking_submit",
                    "booking_direct",
                )
            },
        ),
        (
            "Дякуємо",
            {
                "fields": (
                    "success_title",
                    "success_lead",
                    "success_home",
                    "success_direct",
                )
            },
        ),
    )


@admin.register(LegalSettings)
class LegalSettingsAdmin(SingletonAdmin):
    fieldsets = (
        (
            "Сторінка",
            {"fields": ("privacy_label", "privacy_title", "privacy_body")},
        ),
    )
