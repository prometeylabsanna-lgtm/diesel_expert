from django.db import migrations, models


TEXT_FIXES = (
    ("будь- якої", "будь-якої"),
    ("будь- який", "будь-який"),
    ("будь- яка", "будь-яка"),
    ("будь- якого", "будь-якого"),
    ("будь якої", "будь-якої"),
    ("будь який", "будь-який"),
    ("будь яка", "будь-яка"),
    ("будь якого", "будь-якого"),
    ("турбокомпрессорів", "турбокомпресорів"),
    ("турбокомпрессор", "турбокомпресор"),
    ("(Кодування)", "(кодування)"),
)

OLD_STEERING = (
    "Професійний ремонт рульових рейок усіх типів: "
    "механічних, гідравлічних, електричних"
)
NEW_STEERING = (
    "Професійний ремонт рульових рейок:\n"
    "  механічних\n  гідравлічних\n  електричних"
)


def _apply_fixes(value):
    if not value:
        return value, False
    updated = value.replace(OLD_STEERING, NEW_STEERING)
    for old, new in TEXT_FIXES:
        updated = updated.replace(old, new)
    return updated, updated != value


def forwards(apps, schema_editor):
    SiteSettings = apps.get_model("landing", "SiteSettings")
    HeroCard = apps.get_model("landing", "HeroCard")
    HeroBadge = apps.get_model("landing", "HeroBadge")
    Service = apps.get_model("landing", "Service")

    for site in SiteSettings.objects.all():
        changed = []
        if not site.hero_kicker:
            site.hero_kicker = "СПЕЦІАЛІЗОВАНИЙ АВТОСЕРВІС У ЛУЦЬКУ"
            changed.append("hero_kicker")
        if not site.hero_brand:
            site.hero_brand = "DIESEL EXPERT"
            changed.append("hero_brand")
        if site.hero_title == "Діагностуємо точно - ремонтуємо надійно":
            site.hero_title = "ДІАГНОСТУЄМО ТОЧНО — РЕМОНТУЄМО НАДІЙНО"
            changed.append("hero_title")
        if site.cta_service == "Записатись на сервіс":
            site.cta_service = "Записатись"
            changed.append("cta_service")
        if site.hero_secondary_cta == "Наші послуги":
            site.hero_secondary_cta = "Дізнатись більше"
            changed.append("hero_secondary_cta")
        promo, promo_changed = _apply_fixes(site.promo_text)
        if promo_changed:
            site.promo_text = promo
            changed.append("promo_text")
        if changed:
            site.save(update_fields=changed)

    cards = {
        "Паливна система: діагностика та ремонт": (
            "Паливна система / діагностика та ремонт"
        ),
        "Шліфування ГБЦ та колекторів": "Ремонт ДВЗ",
    }
    for card in HeroCard.objects.all():
        new_title = cards.get(card.title)
        if new_title:
            card.title = new_title
            card.save(update_fields=["title"])

    for badge in HeroBadge.objects.filter(text="Консультація безкоштовно"):
        badge.text = "Консультація безкоштовна"
        badge.save(update_fields=["text"])

    injectors = Service.objects.filter(title="Ремонт форсунок").first()
    pnvt = Service.objects.filter(title="Ремонт ПНВТ").first()
    if (
        injectors
        and pnvt
        and injectors.image_static == "img/services/injectors.webp"
        and pnvt.image_static == "img/services/pnvt.webp"
    ):
        inj_image, pnvt_image = injectors.image.name, pnvt.image.name
        injectors.image_static = "img/services/pnvt.webp"
        pnvt.image_static = "img/services/injectors.webp"
        injectors.image = pnvt_image
        pnvt.image = inj_image
        injectors.save(update_fields=["image", "image_static"])
        pnvt.save(update_fields=["image", "image_static"])

    for service in Service.objects.all():
        title, title_changed = _apply_fixes(service.title)
        bullets, bullets_changed = _apply_fixes(service.bullets)
        fields = []
        if title_changed:
            service.title = title
            fields.append("title")
        if bullets_changed:
            service.bullets = bullets
            fields.append("bullets")
        if fields:
            service.save(update_fields=fields)


def backwards(apps, schema_editor):
    return


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0003_section_visibility"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="hero_kicker",
            field=models.CharField(
                blank=True, max_length=120, verbose_name="Рядок над назвою"
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="hero_brand",
            field=models.CharField(
                blank=True, max_length=80, verbose_name="Назва в першому екрані"
            ),
        ),
        migrations.RunPython(forwards, backwards),
    ]
