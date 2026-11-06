from landing.data import (
    ADVANTAGES,
    BOOKING,
    FAQ_ITEMS,
    HERO,
    HERO_BADGES,
    HERO_CARDS,
    PROMO,
    REVIEWS,
    SERVICES,
    SETTINGS,
    STEPS,
    SUCCESS,
    WORKS,
)
from landing.models import (
    Advantage,
    FaqItem,
    HeroBadge,
    HeroCard,
    MailStep,
    Review,
    Service,
    ServicePrice,
    SiteSettings,
    WorkPhoto,
)

PRIVACY_BODY = """Цей текст тимчасовий і стоїть, доки клієнт не передасть юридичну редакцію.

Diesel Expert обробляє ім’я та номер телефону, які ви залишаєте у формі заявки, щоб передзвонити і узгодити послугу. Дані не продаються і не передаються для реклами третіх осіб.

Заявку бачать лише співробітники сервісу в адмінці, а також — якщо це вказано в налаштуваннях — пошта або Telegram, куди надсилається сповіщення.

Щоб уточнити або видалити заявку, зателефонуйте на номер, вказаний на сайті.
"""


def seed_if_empty():
    _seed_settings()
    _seed_list(Advantage, ADVANTAGES["items"], _advantage)
    _seed_list(HeroCard, HERO_CARDS, _hero_card)
    _seed_list(HeroBadge, HERO_BADGES, _hero_badge)
    _seed_services()
    _seed_list(MailStep, STEPS["items"], _step)
    _seed_list(Review, REVIEWS["items"], _review)
    _seed_list(WorkPhoto, WORKS["items"], _work)
    _seed_list(FaqItem, FAQ_ITEMS, _faq)


def _seed_settings():
    if SiteSettings.objects.filter(pk=1).exists():
        return
    SiteSettings.objects.create(
        phone=SETTINGS["phone"],
        address_line_1=SETTINGS["address_lines"][0],
        address_line_2=SETTINGS["address_lines"][1],
        schedule=SETTINGS["schedule"],
        logo_static=SETTINGS["logo"],
        copyright=SETTINGS["copyright"],
        design_credit=SETTINGS["design_credit"],
        cta_service=SETTINGS["cta_service"],
        cta_diagnostics=SETTINGS["cta_diagnostics"],
        hero_title=HERO["title"],
        hero_image_static=HERO["image"],
        hero_primary_cta=HERO["primary_cta"],
        hero_secondary_cta=HERO["secondary_cta"],
        hero_secondary_url=HERO["secondary_url"],
        advantages_title=ADVANTAGES["title"],
        services_title=SERVICES["title"],
        services_lead=SERVICES["lead"],
        services_more_label=SERVICES["more_label"],
        promo_title=PROMO["title"],
        promo_lead=PROMO["lead"],
        promo_text=PROMO["text"],
        promo_image_static=PROMO["image"],
        promo_cta=PROMO["cta"],
        steps_title=STEPS["title"],
        reviews_title=REVIEWS["title"],
        works_title=WORKS["title"],
        booking_title=BOOKING["title"],
        booking_lead=BOOKING["lead"],
        booking_name_placeholder=BOOKING["name_placeholder"],
        booking_phone_placeholder=BOOKING["phone_placeholder"],
        booking_service_placeholder=BOOKING["service_placeholder"],
        booking_submit=BOOKING["submit"],
        booking_direct=BOOKING["direct"],
        success_title=SUCCESS["title"],
        success_lead=SUCCESS["lead"],
        success_home=SUCCESS["home"],
        success_direct=SUCCESS["direct"],
        privacy_label="Політика конфіденційності",
        privacy_title="Політика конфіденційності",
        privacy_body=PRIVACY_BODY.strip(),
        offer_label="Публічний договір (офферта)",
        offer_title="Публічний договір (офферта)",
        offer_body=(
            "Текст публічного договору тимчасовий і буде замінений "
            "юридичною редакцією клієнта."
        ),
    )


def _seed_list(model, items, builder):
    if model.objects.exists():
        return
    for index, item in enumerate(items, start=1):
        model.objects.create(sort=index, **builder(item))


def _seed_services():
    if Service.objects.exists():
        return
    for index, item in enumerate(SERVICES["items"], start=1):
        service = Service.objects.create(
            title=item["title"],
            image_static=item["image"],
            bullets="\n".join(item["bullets"]),
            wide=item["wide"],
            mobile_extra=item["mobile_extra"],
            sort=index,
        )
        for price_index, price in enumerate(item["prices"], start=1):
            ServicePrice.objects.create(
                service=service,
                label=price["label"],
                short=price["short"],
                value=price["value"],
                sort=price_index,
            )


def _advantage(item):
    return {"icon_static": item["icon"], "title": item["title"], "text": item["text"]}


def _hero_card(item):
    return {
        "title": item["title"],
        "image_static": item["image"],
        "modifier": item["modifier"],
        "url": item["url"],
    }


def _hero_badge(item):
    return {"icon_static": item["icon"], "text": item["text"]}


def _step(item):
    return {"num": item["num"], "title": item["title"], "text": item["text"]}


def _review(item):
    return {"name": item["name"], "text": item["text"]}


def _work(item):
    return {"image_static": item["image"], "alt": item["alt"]}


def _faq(item):
    return {"question": item["question"], "answer": item["answer"]}
