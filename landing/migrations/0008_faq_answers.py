from django.db import migrations

from landing.data import FAQ_ITEMS


def forwards(apps, schema_editor):
    FaqItem = apps.get_model("landing", "FaqItem")
    by_question = {item["question"]: item["answer"] for item in FAQ_ITEMS}
    for row in FaqItem.objects.all():
        answer = by_question.get(row.question)
        if answer and not (row.answer or "").strip():
            row.answer = answer
            row.save(update_fields=["answer"])


def backwards(apps, schema_editor):
    return


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0007_legal_texts_privacy_offer"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
