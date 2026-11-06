"""On-page SEO: title/description, canonical, OG, JSON-LD."""

from __future__ import annotations

import json
from typing import Any
from urllib.parse import urljoin

from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

from landing.images import public_url

BRAND = "Diesel Expert"
HOME_TITLE = (
    "Ремонт дизеля в Луцьку — турбіни, форсунки, ПНВТ | Diesel Expert"
)
HOME_DESCRIPTION = (
    "Діагностика та ремонт дизельних систем у Луцьку: турбіни, форсунки, "
    "ПНВТ, ГБЦ і двигуни. Гарантія на роботи, прийом агрегатів Новою Поштою "
    "по Україні. Запишіться на сервіс."
)


def build_seo(
    request,
    site,
    *,
    url_name: str = "home",
    faq_items: list[dict] | None = None,
    services: list[dict] | None = None,
    page_title: str = "",
    page_description: str = "",
) -> dict[str, Any]:
    origin = _origin(request)
    path = reverse(url_name) if url_name else "/"
    canonical = urljoin(origin + "/", path.lstrip("/"))
    if path == "/":
        canonical = origin + "/"

    og_image = _og_image(request, site)
    robots = "noindex, nofollow" if url_name == "thanks" else "index, follow"

    if url_name == "home":
        title = HOME_TITLE
        description = HOME_DESCRIPTION
    elif url_name == "privacy":
        title = f"{page_title or site.privacy_title} | {BRAND}"
        description = (
            page_description
            or f"Політика конфіденційності {BRAND}: як ми обробляємо дані заявок."
        )
    elif url_name == "offer":
        title = f"{page_title or site.offer_title} | {BRAND}"
        description = (
            page_description
            or f"Публічний договір (оферта) сервісу {BRAND} у Луцьку."
        )
    elif url_name == "thanks":
        title = f"{page_title or site.success_title} | {BRAND}"
        description = page_description or site.success_lead or title
    else:
        title = f"{BRAND} — ремонт дизельних систем у Луцьку"
        description = HOME_DESCRIPTION

    json_ld: list[str] = []
    if url_name == "home":
        json_ld.append(_dumps(_website(origin)))
        json_ld.append(
            _dumps(_local_business(origin, site, og_image, services or []))
        )
        faq_schema = _faq_page(faq_items or [])
        if faq_schema:
            json_ld.append(_dumps(faq_schema))
    elif url_name in ("privacy", "offer"):
        json_ld.append(
            _dumps(
                _breadcrumb(
                    origin,
                    [
                        ("Головна", origin + "/"),
                        (page_title or title.split(" | ")[0], canonical),
                    ],
                )
            )
        )

    return {
        "title": title,
        "description": description,
        "canonical": canonical,
        "robots": robots,
        "og_title": title,
        "og_description": description,
        "og_image": og_image,
        "og_image_width": "1200",
        "og_image_height": "630",
        "og_type": "website",
        "og_locale": "uk_UA",
        "og_url": canonical,
        "json_ld": json_ld,
        "hero_image": _hero_image_url(request, site),
        "hero_preload": url_name == "home",
    }


def _origin(request) -> str:
    if request is None:
        return ""
    return request.build_absolute_uri("/").rstrip("/")


def _abs(request, path: str) -> str:
    if not path:
        return ""
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if request is None:
        return path
    return request.build_absolute_uri(path)


def _hero_image_url(request, site) -> str:
    if site.hero_image and site.hero_image.name:
        return _abs(request, public_url(site.hero_image, ""))
    static_path = staticfiles_storage.url("img/hero/bg.webp")
    return _abs(request, static_path)


def _og_image(request, site) -> str:
    hero = _hero_image_url(request, site)
    if hero:
        return hero
    logo = public_url(site.logo, site.logo_static)
    return _abs(request, logo)


def _website(origin: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": BRAND,
        "url": origin + "/",
        "inLanguage": "uk-UA",
    }


def _local_business(
    origin: str, site, image: str, services: list[dict] | None = None
) -> dict:
    street = (site.address_line_2 or "").replace("вул,", "вул.").strip()
    locality = (site.address_line_1 or "").replace("м.", "").strip()
    data: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "AutoRepair",
        "name": BRAND,
        "url": origin + "/",
        "image": image,
        "telephone": site.phone_href.replace("tel:", "") if site.phone_href else site.phone,
        "priceRange": "₴₴",
        "currenciesAccepted": "UAH",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": street or site.address_line_2 or "",
            "addressLocality": locality or "Луцьк",
            "addressRegion": "Волинська область",
            "addressCountry": "UA",
        },
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                ],
                "opens": "09:00",
                "closes": "19:00",
            },
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": "Saturday",
                "opens": "09:00",
                "closes": "15:00",
            },
        ],
        "areaServed": {
            "@type": "Country",
            "name": "Ukraine",
        },
    }
    if site.logo_static or (site.logo and site.logo.name):
        data["logo"] = image
    catalog = _offer_catalog(origin, services or [])
    if catalog:
        data["hasOfferCatalog"] = catalog
    return data


def _offer_catalog(origin: str, services: list[dict]) -> dict | None:
    elements = []
    for index, service in enumerate(services, start=1):
        title = (service.get("title") or "").strip()
        if not title:
            continue
        offer: dict[str, Any] = {
            "@type": "Offer",
            "itemOffered": {
                "@type": "Service",
                "name": title,
                "provider": {"@type": "AutoRepair", "name": BRAND},
                "areaServed": "UA",
                "url": f"{origin}/#services",
            },
        }
        prices = service.get("prices") or []
        if prices:
            value = (prices[0].get("value") or "").strip()
            if value and value[0].isdigit():
                digits = "".join(ch for ch in value if ch.isdigit())
                if digits:
                    offer["priceCurrency"] = "UAH"
                    offer["price"] = digits
        elements.append(
            {
                "@type": "ListItem",
                "position": index,
                "item": offer,
            }
        )
    if not elements:
        return None
    return {
        "@type": "OfferCatalog",
        "name": "Послуги Diesel Expert",
        "itemListElement": elements,
    }


def _faq_page(items: list[dict]) -> dict | None:
    entities = []
    for item in items:
        question = (item.get("question") or "").strip()
        answer = (item.get("answer") or "").strip()
        if not question or not answer:
            continue
        entities.append(
            {
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {"@type": "Answer", "text": answer},
            }
        )
    if not entities:
        return None
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities,
    }


def _breadcrumb(origin: str, crumbs: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index,
                "name": name,
                "item": url,
            }
            for index, (name, url) in enumerate(crumbs, start=1)
        ],
    }


def _dumps(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
