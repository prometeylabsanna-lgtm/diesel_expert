import re

from django.db import models

from landing.fields import WebPImageField
from landing.images import validate_raster


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class SiteSettings(SingletonModel):
    phone = models.CharField("Телефон", max_length=32)
    phone_href = models.CharField("Посилання tel:", max_length=40, blank=True)
    address_line_1 = models.CharField("Адреса, рядок 1", max_length=120)
    address_line_2 = models.CharField("Адреса, рядок 2", max_length=120, blank=True)
    schedule = models.CharField("Графік", max_length=160)
    logo = WebPImageField(
        "Логотип (файл)",
        upload_to="brand/",
        blank=True,
        validators=[validate_raster],
    )
    logo_static = models.CharField(
        "Логотип із дизайну",
        max_length=200,
        default="img/logo.webp",
        help_text="Використовується, якщо файл не завантажено.",
    )
    copyright = models.CharField("Копірайт", max_length=200)
    design_credit = models.CharField("Підпис дизайну", max_length=200, blank=True)
    cta_service = models.CharField("Кнопка в шапці", max_length=80)
    cta_diagnostics = models.CharField("Кнопка діагностики", max_length=80)

    hero_title = models.CharField("Головна пропозиція", max_length=200)
    hero_image = WebPImageField(
        "Фон першого екрана",
        upload_to="hero/",
        blank=True,
        validators=[validate_raster],
    )
    hero_image_static = models.CharField(
        "Фон із дизайну",
        max_length=200,
        default="img/hero/bg.webp",
    )
    hero_primary_cta = models.CharField("Головна кнопка", max_length=80)
    hero_secondary_cta = models.CharField("Друга кнопка", max_length=80)
    hero_secondary_url = models.CharField("Посилання другої кнопки", max_length=200)

    advantages_title = models.CharField("Заголовок переваг", max_length=160)
    services_title = models.CharField("Заголовок послуг", max_length=160)
    services_lead = models.CharField("Підзаголовок послуг", max_length=240)
    services_more_label = models.CharField("Кнопка «ще»", max_length=80)
    promo_title = models.CharField("Заголовок Нової пошти", max_length=200)
    promo_lead = models.TextField("Лід Нової пошти", blank=True)
    promo_text = models.TextField("Текст Нової пошти", blank=True)
    promo_image = WebPImageField(
        "Фото Нової пошти",
        upload_to="promo/",
        blank=True,
        validators=[validate_raster],
    )
    promo_image_static = models.CharField(
        "Фото Нової пошти із дизайну",
        max_length=200,
        default="img/promo.webp",
    )
    promo_cta = models.CharField("Кнопка Нової пошти", max_length=80, blank=True)
    steps_title = models.CharField("Заголовок кроків", max_length=160)
    reviews_title = models.CharField("Заголовок відгуків", max_length=160)
    works_title = models.CharField("Заголовок робіт", max_length=160)

    booking_title = models.CharField("Заголовок форми", max_length=120)
    booking_lead = models.TextField("Текст форми")
    booking_name_placeholder = models.CharField("Плейсхолдер імені", max_length=80)
    booking_phone_placeholder = models.CharField("Плейсхолдер телефону", max_length=80)
    booking_service_placeholder = models.CharField("Плейсхолдер послуги", max_length=80)
    booking_submit = models.CharField("Кнопка форми", max_length=80)
    booking_direct = models.CharField("Текст під формою", max_length=120)
    success_title = models.CharField("Заголовок «дякуємо»", max_length=120)
    success_lead = models.TextField("Текст «дякуємо»")
    success_home = models.CharField("Кнопка на головну", max_length=80)
    success_direct = models.CharField("Текст під «дякуємо»", max_length=120)

    privacy_label = models.CharField("Підпис посилання", max_length=120)
    privacy_title = models.CharField("Заголовок політики", max_length=160)
    privacy_body = models.TextField("Текст політики")
    offer_label = models.CharField(
        "Підпис оферти",
        max_length=120,
        default="Публічний договір (офферта)",
    )
    offer_title = models.CharField(
        "Заголовок оферти",
        max_length=160,
        default="Публічний договір (офферта)",
    )
    offer_body = models.TextField(
        "Текст оферти",
        blank=True,
        default=(
            "Текст публічного договору тимчасовий і буде замінений "
            "юридичною редакцією клієнта."
        ),
    )

    notify_email = models.EmailField(
        "Пошта для заявок",
        blank=True,
        help_text="Порожнє поле — лист не надсилається.",
    )
    telegram_bot_token = models.CharField(
        "Telegram bot token",
        max_length=128,
        blank=True,
        help_text="Не показується на сайті.",
    )
    telegram_chat_id = models.CharField("Telegram chat id", max_length=64, blank=True)

    class Meta:
        verbose_name = "Налаштування сайту"
        verbose_name_plural = "Налаштування сайту"

    def __str__(self):
        return "Налаштування сайту"

    def save(self, *args, **kwargs):
        digits = re.sub(r"\D", "", self.phone or "")
        if digits.startswith("0"):
            digits = "38" + digits
        self.phone_href = f"tel:+{digits}" if digits else ""
        super().save(*args, **kwargs)


class ContactsSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Контакти"
        verbose_name_plural = "Контакти"


class HeroSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Перший екран"
        verbose_name_plural = "Перший екран"


class AdvantagesSectionSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Секція «Переваги»"
        verbose_name_plural = "Секція «Переваги»"


class ServicesSectionSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Секція «Послуги»"
        verbose_name_plural = "Секція «Послуги»"


class PromoSectionSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Секція «Нова пошта»"
        verbose_name_plural = "Секція «Нова пошта»"


class StepsSectionSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Секція «Кроки»"
        verbose_name_plural = "Секція «Кроки»"


class ReviewsSectionSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Секція «Відгуки»"
        verbose_name_plural = "Секція «Відгуки»"


class WorksSectionSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Секція «Роботи»"
        verbose_name_plural = "Секція «Роботи»"


class BookingSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Форма заявки"
        verbose_name_plural = "Форма заявки"


class PrivacySettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Політика конфіденційності"
        verbose_name_plural = "Політика конфіденційності"


class OfferSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Публічний договір"
        verbose_name_plural = "Публічний договір"


# Зворотна сумісність імпортів
SectionSettings = AdvantagesSectionSettings
LegalSettings = PrivacySettings
