from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0002_admin_cms_webp_offer_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="show_advantages_section",
            field=models.BooleanField(default=True, verbose_name="Показувати блок"),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="show_services_section",
            field=models.BooleanField(default=True, verbose_name="Показувати блок"),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="show_promo_section",
            field=models.BooleanField(default=True, verbose_name="Показувати блок"),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="show_steps_section",
            field=models.BooleanField(default=True, verbose_name="Показувати блок"),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="show_reviews_section",
            field=models.BooleanField(default=True, verbose_name="Показувати блок"),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="show_works_section",
            field=models.BooleanField(default=True, verbose_name="Показувати блок"),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="show_faq_section",
            field=models.BooleanField(default=True, verbose_name="Показувати блок"),
        ),
        migrations.CreateModel(
            name="FaqSectionSettings",
            fields=[],
            options={
                "verbose_name": "Секція «Питання»",
                "verbose_name_plural": "Секція «Питання»",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("landing.sitesettings",),
        ),
    ]
