from django.db import migrations, models

from landing.legal_texts import OFFER_BODY, PRIVACY_BODY


def forwards(apps, schema_editor):
    SiteSettings = apps.get_model("landing", "SiteSettings")
    for site in SiteSettings.objects.all():
        site.privacy_body = PRIVACY_BODY
        site.offer_body = OFFER_BODY
        site.offer_label = "Публічний договір (оферта)"
        site.offer_title = "Публічний договір (оферта)"
        site.privacy_label = "Політика конфіденційності"
        site.privacy_title = "Політика конфіденційності"
        site.save(
            update_fields=[
                "privacy_body",
                "offer_body",
                "offer_label",
                "offer_title",
                "privacy_label",
                "privacy_title",
            ]
        )


def backwards(apps, schema_editor):
    return


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0006_hide_reviews_by_default"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
        migrations.AlterField(
            model_name="sitesettings",
            name="offer_body",
            field=models.TextField(
                blank=True,
                default="",
                verbose_name="Текст оферти",
            ),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="offer_label",
            field=models.CharField(
                default="Публічний договір (оферта)",
                max_length=120,
                verbose_name="Підпис оферти",
            ),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="offer_title",
            field=models.CharField(
                default="Публічний договір (оферта)",
                max_length=160,
                verbose_name="Заголовок оферти",
            ),
        ),
    ]
