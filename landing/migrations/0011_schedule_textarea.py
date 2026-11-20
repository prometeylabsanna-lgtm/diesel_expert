from django.db import migrations, models


PROPER_SCHEDULE = (
    "Робочий час з 9.00 до 19.00\n"
    "Субота з 9.00 до 15.00\n"
    "Неділя вихідний"
)


def restore_schedule_lines(apps, schema_editor):
    SiteSettings = apps.get_model("landing", "SiteSettings")
    jammed = PROPER_SCHEDULE.replace("\n", "")
    spaced = PROPER_SCHEDULE.replace("\n", " ")
    for row in SiteSettings.objects.all():
        current = (row.schedule or "").replace("\r\n", "\n").strip()
        if current in {jammed, spaced}:
            row.schedule = PROPER_SCHEDULE
            row.save(update_fields=["schedule"])


class Migration(migrations.Migration):

    dependencies = [
        ("landing", "0010_site_look_colors"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sitesettings",
            name="schedule",
            field=models.TextField(verbose_name="Графік"),
        ),
        migrations.RunPython(restore_schedule_lines, migrations.RunPython.noop),
    ]
