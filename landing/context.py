from urllib.parse import quote_plus

from django.urls import reverse

from landing.data import NAV
from landing.images import public_url
from landing.models import (
    Advantage,
    FaqItem,
    HeroBadge,
    HeroCard,
    MailStep,
    Review,
    Service,
    SiteSettings,
    WorkPhoto,
)
from landing.seed import seed_if_empty


def build_context(request=None):
    seed_if_empty()
    site = SiteSettings.objects.get(pk=1)
    on_home = bool(request and getattr(request.resolver_match, "url_name", "") == "home")
    return {
        "nav": _nav(on_home),
        "settings": _settings(site),
        "hero": _hero(site),
        "hero_cards": [_hero_card(item) for item in HeroCard.objects.published()],
        "hero_badges": [_badge(item) for item in HeroBadge.objects.published()],
        "advantages": {
            "title": site.advantages_title,
            "items": [_advantage(item) for item in Advantage.objects.published()],
        },
        "services": {
            "title": site.services_title,
            "lead": site.services_lead,
            "more_label": site.services_more_label,
            "items": [
                _service(item)
                for item in Service.objects.published().prefetch_related("prices")
            ],
        },
        "promo": _promo(site),
        "steps": {
            "title": site.steps_title,
            "items": [
                {"num": item.num, "title": item.title, "text": item.text}
                for item in MailStep.objects.published()
            ],
        },
        "reviews": {
            "title": site.reviews_title,
            "items": [
                {"name": item.name, "initial": item.initial, "text": item.text}
                for item in Review.objects.published()
            ],
        },
        "works": {
            "title": site.works_title,
            "items": [_work(item) for item in WorkPhoto.objects.published()],
        },
        "faq_items": [
            {"question": item.question, "answer": item.answer, "order": item.sort}
            for item in FaqItem.objects.published()
        ],
        "booking": {
            "title": site.booking_title,
            "lead": site.booking_lead,
            "name_placeholder": site.booking_name_placeholder,
            "phone_placeholder": site.booking_phone_placeholder,
            "service_placeholder": site.booking_service_placeholder,
            "submit": site.booking_submit,
            "direct": site.booking_direct,
        },
        "success": {
            "title": site.success_title,
            "lead": site.success_lead,
            "home": site.success_home,
            "direct": site.success_direct,
        },
        "legal": {"title": site.privacy_title, "body": site.privacy_body},
        "offer": {"title": site.offer_title, "body": site.offer_body},
    }


def _nav(on_home):
    home = reverse("home")
    items = []
    for item in NAV:
        url = item["url"]
        if url.startswith("#") and not on_home:
            url = f"{home}{url}"
        items.append({"label": item["label"], "url": url})
    return items


def _settings(site):
    lines = [site.address_line_1]
    if site.address_line_2:
        lines.append(site.address_line_2)
    address_query = ", ".join(part.strip() for part in lines if part and part.strip())
    map_q = quote_plus(address_query)
    legal_links = [
        {"label": site.privacy_label, "url": reverse("privacy")},
        {
            "label": site.offer_label or "Публічний договір (офферта)",
            "url": reverse("offer"),
        },
    ]
    return {
        "phone": site.phone,
        "phone_href": site.phone_href,
        "address_lines": lines,
        "map_embed_url": (
            f"https://maps.google.com/maps?q={map_q}&hl=uk&z=16&output=embed"
        ),
        "map_link_url": f"https://www.google.com/maps/search/?api=1&query={map_q}",
        "logo_url": public_url(site.logo, site.logo_static),
        "schedule": site.schedule,
        "copyright": site.copyright,
        "design_credit": site.design_credit,
        "cta_service": site.cta_service,
        "cta_diagnostics": site.cta_diagnostics,
        "privacy_url": reverse("privacy"),
        "privacy_label": site.privacy_label,
        "legal_links": legal_links,
    }


def _hero(site):
    override = ""
    if site.hero_image and site.hero_image.name:
        override = public_url(site.hero_image, "")
    return {
        "title": site.hero_title,
        "primary_cta": site.hero_primary_cta,
        "secondary_cta": site.hero_secondary_cta,
        "secondary_url": site.hero_secondary_url,
        "bg_override": override,
    }


def _hero_card(item):
    return {
        "title": item.title,
        "modifier": item.modifier,
        "url": item.url,
    }


def _badge(item):
    return {"icon": public_url(item.icon, item.icon_static), "text": item.text}


def _advantage(item):
    return {
        "icon": public_url(item.icon, item.icon_static),
        "title": item.title,
        "text": item.text,
    }


def _service(item):
    return {
        "title": item.title,
        "image": public_url(item.image, item.image_static),
        "bullets": item.bullet_list(),
        "prices": [
            {"label": price.label, "short": price.short, "value": price.value}
            for price in item.prices.all()
        ],
        "wide": item.wide,
        "mobile_extra": item.mobile_extra,
    }


def _promo(site):
    return {
        "title": site.promo_title,
        "lead": site.promo_lead,
        "text": site.promo_text,
        "image": public_url(site.promo_image, site.promo_image_static),
        "cta": site.promo_cta,
    }


def _work(item):
    return {"image": public_url(item.image, item.image_static), "alt": item.alt}
