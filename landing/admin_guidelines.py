"""Підказки CMS: ліміти тексту та профілі зображень."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ImageProfile:
    label: str
    width: int
    height: int
    max_kb: int

    @property
    def hint(self) -> str:
        return (
            f"Рекомендовано {self.width}×{self.height} px, "
            f"JPG/PNG/WebP, до {self.max_kb} КБ. "
            "Після завантаження файл автоматично стане WebP. "
            "Превʼю нижче — поточне фото на сайті."
        )


@dataclass(frozen=True)
class TextLimit:
    max_chars: int
    soft: bool = False

    @property
    def hint(self) -> str:
        if self.soft:
            return f"Бажано до {self.max_chars} символів, щоб блок виглядав акуратно."
        return f"Не більше {self.max_chars} символів."


IMAGE_PROFILES: dict[str, ImageProfile] = {
    "hero": ImageProfile("Фон першого екрана", 1440, 1020, 900),
    "logo": ImageProfile("Логотип", 384, 332, 200),
    "promo": ImageProfile("Фото Нової пошти", 660, 469, 500),
    "service": ImageProfile("Фото послуги", 640, 480, 450),
    "work": ImageProfile("Фото роботи", 980, 574, 500),
    "icon": ImageProfile("Іконка", 80, 80, 80),
    "map": ImageProfile("Карта", 640, 332, 300),
    "default": ImageProfile("Зображення", 1200, 800, 700),
}

TEXT_LIMITS: dict[str, TextLimit] = {
    "phone": TextLimit(32),
    "address_line_1": TextLimit(120),
    "address_line_2": TextLimit(120),
    "schedule": TextLimit(160, soft=True),
    "copyright": TextLimit(200),
    "design_credit": TextLimit(200),
    "cta_service": TextLimit(40),
    "cta_diagnostics": TextLimit(40),
    "hero_title": TextLimit(90),
    "hero_primary_cta": TextLimit(40),
    "hero_secondary_cta": TextLimit(40),
    "advantages_title": TextLimit(80),
    "services_title": TextLimit(80),
    "services_lead": TextLimit(180, soft=True),
    "services_more_label": TextLimit(40),
    "promo_title": TextLimit(120),
    "promo_lead": TextLimit(200, soft=True),
    "promo_text": TextLimit(600, soft=True),
    "promo_cta": TextLimit(40),
    "steps_title": TextLimit(80),
    "reviews_title": TextLimit(80),
    "works_title": TextLimit(80),
    "booking_title": TextLimit(120),
    "booking_lead": TextLimit(280, soft=True),
    "booking_name_placeholder": TextLimit(80),
    "booking_phone_placeholder": TextLimit(80),
    "booking_service_placeholder": TextLimit(80),
    "booking_submit": TextLimit(80),
    "booking_direct": TextLimit(120),
    "success_title": TextLimit(120),
    "success_lead": TextLimit(280, soft=True),
    "success_home": TextLimit(80),
    "success_direct": TextLimit(120),
    "privacy_label": TextLimit(120),
    "privacy_title": TextLimit(160),
    "privacy_body": TextLimit(20000, soft=True),
    "offer_label": TextLimit(120),
    "offer_title": TextLimit(160),
    "offer_body": TextLimit(20000, soft=True),
    "title": TextLimit(120),
    "text": TextLimit(400, soft=True),
    "name": TextLimit(80),
    "question": TextLimit(240),
    "answer": TextLimit(4000, soft=True),
    "bullets": TextLimit(800, soft=True),
    "alt": TextLimit(160),
    "num": TextLimit(8),
}

TINYMCE_FIELDS = frozenset(
    {
        "privacy_body",
        "offer_body",
        "answer",
        "promo_text",
        "booking_lead",
        "success_lead",
    }
)

HELP_EXTRA: dict[str, str] = {
    "schedule": "Кожен рядок — окремий рядок у підвалі сайту.",
    "bullets": "Кожен пункт з нового рядка — так і з’явиться в картці послуги.",
    "wide": "Увімкніть для широкої картки в сітці послуг.",
    "mobile_extra": "На телефоні картка з’явиться після кнопки «ще».",
    "logo_static": "Запасний логотип з дизайну, якщо файл вище не завантажено.",
    "hero_image_static": "Запасне фото з дизайну, якщо файл вище не завантажено.",
    "promo_image_static": "Запасне фото з дизайну, якщо файл вище не завантажено.",
    "image_static": "Запасне фото з дизайну, якщо файл вище не завантажено.",
    "icon_static": "Запасна іконка з дизайну, якщо файл вище не завантажено.",
    "slug": "Створюється автоматично з назви. Потрібен для внутрішніх посилань.",
    "modifier": "Технічний код стилю. Створюється автоматично.",
    "notify_email": "Куди надсилати нові заявки. Порожнє — листи не йдуть.",
    "telegram_bot_token": "Секрет бота. Не показується на сайті.",
    "telegram_chat_id": "ID чату для сповіщень про заявки.",
}


def image_profile_for_field(name: str) -> ImageProfile:
    low = (name or "").lower()
    if "logo" in low:
        return IMAGE_PROFILES["logo"]
    if "hero" in low:
        return IMAGE_PROFILES["hero"]
    if "promo" in low:
        return IMAGE_PROFILES["promo"]
    if "service" in low or name == "image":
        return IMAGE_PROFILES["service"] if "work" not in low else IMAGE_PROFILES["work"]
    if "work" in low:
        return IMAGE_PROFILES["work"]
    if "icon" in low:
        return IMAGE_PROFILES["icon"]
    if "map" in low:
        return IMAGE_PROFILES["map"]
    return IMAGE_PROFILES["default"]


def text_limit_for_field(name: str) -> TextLimit | None:
    if name in TEXT_LIMITS:
        return TEXT_LIMITS[name]
    if name.endswith("_cta") or name.endswith("_label"):
        return TextLimit(40)
    if name.endswith("_title"):
        return TextLimit(100)
    if name.endswith("_lead") or name.endswith("_text") or name.endswith("_body"):
        return TextLimit(800, soft=True)
    if name.endswith("_placeholder"):
        return TextLimit(80)
    return None


def help_for_field(name: str) -> str:
    parts: list[str] = []
    if name in HELP_EXTRA:
        parts.append(HELP_EXTRA[name])
    if name.endswith("_image") or name in {"logo", "icon", "image"} or "image" in name:
        if not name.endswith("_static"):
            parts.append(image_profile_for_field(name).hint)
    limit = text_limit_for_field(name)
    if limit and "image" not in name and not name.endswith("_static"):
        parts.append(limit.hint)
    return " ".join(parts)
