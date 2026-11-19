from django.db import migrations, models


def hide_reviews(apps, schema_editor):
    SiteSettings = apps.get_model("landing", "SiteSettings")
    SiteSettings.objects.update(show_reviews_section=False)


def show_reviews(apps, schema_editor):
    SiteSettings = apps.get_model("landing", "SiteSettings")
    SiteSettings.objects.update(show_reviews_section=True)


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0005_steering_list_punctuation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sitesettings",
            name="show_reviews_section",
            field=models.BooleanField(default=False, verbose_name="Показувати блок"),
        ),
        migrations.RunPython(hide_reviews, show_reviews),
    ]
