from django.db import models
from django.utils.text import slugify

from landing.fields import WebPImageField
from landing.images import validate_raster


class OrderedQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)


class Advantage(models.Model):
    icon = WebPImageField(
        "Іконка (файл)",
        upload_to="icons/",
        blank=True,
        validators=[validate_raster],
    )
    icon_static = models.CharField("Іконка із дизайну", max_length=200)
    title = models.CharField("Заголовок", max_length=80)
    text = models.TextField("Текст")
    sort = models.PositiveIntegerField("Порядок", default=0)
    is_published = models.BooleanField("На сайті", default=True)

    objects = OrderedQuerySet.as_manager()

    class Meta:
        ordering = ("sort", "id")
        verbose_name = "Перевага"
        verbose_name_plural = "Переваги"

    def __str__(self):
        return self.title


class HeroCard(models.Model):
    title = models.CharField("Назва", max_length=160)
    image_static = models.CharField("Маска із дизайну", max_length=200)
    modifier = models.SlugField("Модифікатор CSS", max_length=32, blank=True)
    url = models.CharField("Посилання", max_length=200, blank=True)
    sort = models.PositiveIntegerField("Порядок", default=0)
    is_published = models.BooleanField("На сайті", default=True)

    objects = OrderedQuerySet.as_manager()

    class Meta:
        ordering = ("sort", "id")
        verbose_name = "Картка напрямку"
        verbose_name_plural = "Картки напрямків"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.modifier:
            self.modifier = slugify(self.title, allow_unicode=True)[:32] or "card"
        super().save(*args, **kwargs)


class HeroBadge(models.Model):
    icon = WebPImageField(
        "Іконка (файл)",
        upload_to="icons/",
        blank=True,
        validators=[validate_raster],
    )
    icon_static = models.CharField("Іконка із дизайну", max_length=200)
    text = models.CharField("Текст", max_length=120)
    sort = models.PositiveIntegerField("Порядок", default=0)
    is_published = models.BooleanField("На сайті", default=True)

    objects = OrderedQuerySet.as_manager()

    class Meta:
        ordering = ("sort", "id")
        verbose_name = "Плашка першого екрана"
        verbose_name_plural = "Плашки першого екрана"

    def __str__(self):
        return self.text


class Service(models.Model):
    title = models.CharField("Назва", max_length=200)
    slug = models.SlugField("Slug", max_length=160, blank=True, unique=True)
    image = WebPImageField(
        "Фото",
        upload_to="services/",
        blank=True,
        validators=[validate_raster],
    )
    image_static = models.CharField("Фото із дизайну", max_length=200)
    bullets = models.TextField("Пункти", help_text="Кожен пункт з нового рядка.")
    wide = models.BooleanField("Широка картка", default=False)
    mobile_extra = models.BooleanField("Ховається на телефоні до «ще»", default=False)
    sort = models.PositiveIntegerField("Порядок", default=0)
    is_published = models.BooleanField("На сайті", default=True)

    objects = OrderedQuerySet.as_manager()

    class Meta:
        ordering = ("sort", "id")
        verbose_name = "Послуга"
        verbose_name_plural = "Послуги"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title, allow_unicode=True)[:150] or "service"
            slug = base
            n = 2
            while Service.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def bullet_list(self):
        return [line.strip() for line in self.bullets.splitlines() if line.strip()]


class ServicePrice(models.Model):
    service = models.ForeignKey(
        Service,
        related_name="prices",
        on_delete=models.CASCADE,
        verbose_name="Послуга",
    )
    label = models.CharField("Підпис", max_length=80)
    short = models.CharField("Короткий підпис", max_length=40)
    value = models.CharField("Ціна", max_length=80)
    sort = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ("sort", "id")
        verbose_name = "Ціна"
        verbose_name_plural = "Ціни"

    def __str__(self):
        return f"{self.label} {self.value}"


class MailStep(models.Model):
    num = models.CharField("Номер", max_length=8)
    title = models.CharField("Заголовок", max_length=120)
    text = models.TextField("Текст")
    sort = models.PositiveIntegerField("Порядок", default=0)
    is_published = models.BooleanField("На сайті", default=True)

    objects = OrderedQuerySet.as_manager()

    class Meta:
        ordering = ("sort", "id")
        verbose_name = "Крок ремонту поштою"
        verbose_name_plural = "Кроки ремонту поштою"

    def __str__(self):
        return f"{self.num} {self.title}"


class Review(models.Model):
    name = models.CharField("Ім’я", max_length=80)
    text = models.TextField("Текст")
    sort = models.PositiveIntegerField("Порядок", default=0)
    is_published = models.BooleanField("На сайті", default=True)

    objects = OrderedQuerySet.as_manager()

    class Meta:
        ordering = ("sort", "id")
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"

    def __str__(self):
        return self.name

    @property
    def initial(self):
        stripped = self.name.strip()
        return stripped[:1].upper() if stripped else ""


class WorkPhoto(models.Model):
    image = WebPImageField(
        "Фото",
        upload_to="works/",
        blank=True,
        validators=[validate_raster],
    )
    image_static = models.CharField("Фото із дизайну", max_length=200)
    alt = models.CharField("Підпис", max_length=160, blank=True)
    sort = models.PositiveIntegerField("Порядок", default=0)
    is_published = models.BooleanField("На сайті", default=True)

    objects = OrderedQuerySet.as_manager()

    class Meta:
        ordering = ("sort", "id")
        verbose_name = "Робота"
        verbose_name_plural = "Роботи"

    def __str__(self):
        return self.alt or f"Фото {self.pk or ''}".strip()


class FaqItem(models.Model):
    question = models.CharField("Питання", max_length=240)
    answer = models.TextField("Відповідь", blank=True)
    sort = models.PositiveIntegerField("Порядок", default=0)
    is_published = models.BooleanField("На сайті", default=True)

    objects = OrderedQuerySet.as_manager()

    class Meta:
        ordering = ("sort", "id")
        verbose_name = "Питання"
        verbose_name_plural = "Питання й відповіді"

    def __str__(self):
        return self.question
