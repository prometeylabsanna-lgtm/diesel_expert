from django.db import migrations

COOKIE_NOTE = (
    "Сайт збирає файли cookie. Вони потрібні для стабільної роботи сторінок, "
    "безпеки форм і щоб запам’ятати вашу згоду або відмову в банері cookie. "
    "Маркетингові cookie третіх осіб ми не ставимо. Погодитись або відмовитись "
    "можна в банері; вибір зберігається у вашому браузері."
)


def _mentions_cookies(value: str) -> bool:
    text = (value or "").lower()
    return "cookie" in text or "кукі" in text or "куки" in text


def forwards(apps, schema_editor):
    SiteSettings = apps.get_model("landing", "SiteSettings")
    for site in SiteSettings.objects.all():
        body = site.privacy_body or ""
        if _mentions_cookies(body):
            continue
        if "<" in body and ">" in body:
            site.privacy_body = body.rstrip() + f"<p>{COOKIE_NOTE}</p>"
        else:
            site.privacy_body = (body.rstrip() + "\n\n" + COOKIE_NOTE).strip()
        site.save(update_fields=["privacy_body"])


def backwards(apps, schema_editor):
    return


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0008_faq_answers"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
