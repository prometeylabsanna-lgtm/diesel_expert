from django.contrib import admin

from landing.admin_mixins import SingletonAdmin
from landing.models import (
    AdvantagesSectionSettings,
    BookingSettings,
    ContactsSettings,
    FaqSectionSettings,
    HeroSettings,
    OfferSettings,
    PrivacySettings,
    PromoSectionSettings,
    ReviewsSectionSettings,
    ServicesSectionSettings,
    StepsSectionSettings,
    WorksSectionSettings,
)

@admin.register(ContactsSettings)
class ContactsSettingsAdmin(SingletonAdmin):
    fieldsets = (
        (
            "Контакти",
            {"fields": ("phone", "address_line_1", "address_line_2", "schedule")},
        ),
        ("Логотип", {"fields": ("logo",)}),
        (
            "Запас із дизайну",
            {
                "classes": ("collapse",),
                "fields": ("logo_static",),
            },
        ),
        ("Кнопки", {"fields": ("cta_service", "cta_diagnostics")}),
        ("Підвал", {"fields": ("copyright",)}),
        (
            "Сповіщення",
            {"fields": ("notify_email", "telegram_bot_token", "telegram_chat_id")},
        ),
    )


@admin.register(HeroSettings)
class HeroSettingsAdmin(SingletonAdmin):
    fieldsets = (
        (
            "Тексти",
            {
                "fields": (
                    "hero_title",
                    "hero_primary_cta",
                    "hero_secondary_cta",
                    "hero_secondary_url",
                )
            },
        ),
        ("Фон", {"fields": ("hero_image",)}),
        (
            "Запас із дизайну",
            {
                "classes": ("collapse",),
                "fields": ("hero_image_static",),
            },
        ),
    )


@admin.register(AdvantagesSectionSettings)
class AdvantagesSectionSettingsAdmin(SingletonAdmin):
    fieldsets = (
        ("Видимість", {"fields": ("show_advantages_section",)}),
        ("Заголовок блоку", {"fields": ("advantages_title",)}),
    )


@admin.register(ServicesSectionSettings)
class ServicesSectionSettingsAdmin(SingletonAdmin):
    fieldsets = (
        ("Видимість", {"fields": ("show_services_section",)}),
        (
            "Заголовки блоку",
            {
                "fields": (
                    "services_title",
                    "services_lead",
                    "services_more_label",
                )
            },
        ),
    )


@admin.register(PromoSectionSettings)
class PromoSectionSettingsAdmin(SingletonAdmin):
    fieldsets = (
        ("Видимість", {"fields": ("show_promo_section",)}),
        (
            "Тексти",
            {
                "fields": (
                    "promo_title",
                    "promo_lead",
                    "promo_text",
                    "promo_cta",
                )
            },
        ),
        ("Фото", {"fields": ("promo_image",)}),
        (
            "Запас із дизайну",
            {
                "classes": ("collapse",),
                "fields": ("promo_image_static",),
            },
        ),
    )


@admin.register(StepsSectionSettings)
class StepsSectionSettingsAdmin(SingletonAdmin):
    fieldsets = (
        ("Видимість", {"fields": ("show_steps_section",)}),
        ("Заголовок блоку", {"fields": ("steps_title",)}),
    )


@admin.register(ReviewsSectionSettings)
class ReviewsSectionSettingsAdmin(SingletonAdmin):
    fieldsets = (
        ("Видимість", {"fields": ("show_reviews_section",)}),
        ("Заголовок блоку", {"fields": ("reviews_title",)}),
    )


@admin.register(WorksSectionSettings)
class WorksSectionSettingsAdmin(SingletonAdmin):
    fieldsets = (
        ("Видимість", {"fields": ("show_works_section",)}),
        ("Заголовок блоку", {"fields": ("works_title",)}),
    )


@admin.register(FaqSectionSettings)
class FaqSectionSettingsAdmin(SingletonAdmin):
    fieldsets = (("Видимість", {"fields": ("show_faq_section",)}),)


@admin.register(BookingSettings)
class BookingSettingsAdmin(SingletonAdmin):
    fieldsets = (
        (
            "Форма запису",
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
            "Екран «Дякуємо»",
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


@admin.register(PrivacySettings)
class PrivacySettingsAdmin(SingletonAdmin):
    fieldsets = (
        (
            "Сторінка політики",
            {"fields": ("privacy_label", "privacy_title", "privacy_body")},
        ),
    )


@admin.register(OfferSettings)
class OfferSettingsAdmin(SingletonAdmin):
    fieldsets = (
        (
            "Сторінка публічного договору",
            {"fields": ("offer_label", "offer_title", "offer_body")},
        ),
    )
