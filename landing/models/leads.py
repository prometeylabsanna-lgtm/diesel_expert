from django.db import models


class Lead(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Нова"
        IN_PROGRESS = "in_progress", "В роботі"
        DONE = "done", "Опрацьована"
        CANCELLED = "cancelled", "Скасована"

    name = models.CharField("Ім’я", max_length=80)
    phone = models.CharField("Телефон", max_length=20)
    service_title = models.CharField("Послуга", max_length=200)
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        db_index=True,
    )
    created_at = models.DateTimeField("Надіслано", auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"{self.name} · {self.phone}"
