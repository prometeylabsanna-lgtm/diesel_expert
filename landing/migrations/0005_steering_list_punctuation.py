from django.db import migrations

OLD = (
    "Професійний ремонт рульових рейок:\n"
    "  механічних\n  гідравлічних\n  електричних"
)
NEW = (
    "Професійний ремонт рульових рейок:\n"
    "  механічних,\n  гідравлічних,\n  електричних."
)


def forwards(apps, schema_editor):
    Service = apps.get_model("landing", "Service")
    for service in Service.objects.filter(title="Ремонт рульових рейок"):
        if OLD not in service.bullets:
            continue
        service.bullets = service.bullets.replace(OLD, NEW)
        service.save(update_fields=["bullets"])


def backwards(apps, schema_editor):
    Service = apps.get_model("landing", "Service")
    for service in Service.objects.filter(title="Ремонт рульових рейок"):
        if NEW not in service.bullets:
            continue
        service.bullets = service.bullets.replace(NEW, OLD)
        service.save(update_fields=["bullets"])


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0004_hero_copy_fixes"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
